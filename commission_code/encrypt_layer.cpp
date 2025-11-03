// encrypt_layer.cpp
// AES-256-GCM file encrypt/decrypt helper using OpenSSL EVP API.
// Build: g++ encrypt_layer.cpp -lcrypto -o encrypt_layer

#include <openssl/evp.h>
#include <openssl/rand.h>
#include <fstream>
#include <vector>
#include <iostream>
#include <string>

static const int KEY_LEN = 32; // 256 bits
static const int IV_LEN = 12;  // 96 bits recommended for GCM
static const int TAG_LEN = 16;

bool aes_gcm_encrypt(const std::vector<unsigned char>& key,
                     const std::vector<unsigned char>& plaintext,
                     std::vector<unsigned char>& out_iv,
                     std::vector<unsigned char>& ciphertext,
                     std::vector<unsigned char>& tag) {
    EVP_CIPHER_CTX* ctx = EVP_CIPHER_CTX_new();
    if (!ctx) return false;

    out_iv.resize(IV_LEN);
    if (RAND_bytes(out_iv.data(), IV_LEN) != 1) {
        EVP_CIPHER_CTX_free(ctx);
        return false;
    }

    if (EVP_EncryptInit_ex(ctx, EVP_aes_256_gcm(), NULL, NULL, NULL) != 1) {
        EVP_CIPHER_CTX_free(ctx);
        return false;
    }

    if (EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_GCM_SET_IVLEN, IV_LEN, NULL) != 1) {
        EVP_CIPHER_CTX_free(ctx);
        return false;
    }

    if (EVP_EncryptInit_ex(ctx, NULL, NULL, key.data(), out_iv.data()) != 1) {
        EVP_CIPHER_CTX_free(ctx);
        return false;
    }

    int len = 0;
    ciphertext.resize(plaintext.size());
    if (EVP_EncryptUpdate(ctx, ciphertext.data(), &len, plaintext.data(), (int)plaintext.size()) != 1) {
        EVP_CIPHER_CTX_free(ctx);
        return false;
    }
    int ciphertext_len = len;

    if (EVP_EncryptFinal_ex(ctx, ciphertext.data() + len, &len) != 1) {
        EVP_CIPHER_CTX_free(ctx);
        return false;
    }
    ciphertext_len += len;
    ciphertext.resize(ciphertext_len);

    tag.resize(TAG_LEN);
    if (EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_GCM_GET_TAG, TAG_LEN, tag.data()) != 1) {
        EVP_CIPHER_CTX_free(ctx);
        return false;
    }

    EVP_CIPHER_CTX_free(ctx);
    return true;
}

bool aes_gcm_decrypt(const std::vector<unsigned char>& key,
                     const std::vector<unsigned char>& iv,
                     const std::vector<unsigned char>& ciphertext,
                     const std::vector<unsigned char>& tag,
                     std::vector<unsigned char>& plaintext_out) {
    EVP_CIPHER_CTX* ctx = EVP_CIPHER_CTX_new();
    if (!ctx) return false;

    if (EVP_DecryptInit_ex(ctx, EVP_aes_256_gcm(), NULL, NULL, NULL) != 1) {
        EVP_CIPHER_CTX_free(ctx);
        return false;
    }

    if (EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_GCM_SET_IVLEN, iv.size(), NULL) != 1) {
        EVP_CIPHER_CTX_free(ctx);
        return false;
    }

    if (EVP_DecryptInit_ex(ctx, NULL, NULL, key.data(), iv.data()) != 1) {
        EVP_CIPHER_CTX_free(ctx);
        return false;
    }

    int len = 0;
    plaintext_out.resize(ciphertext.size());
    if (EVP_DecryptUpdate(ctx, plaintext_out.data(), &len, ciphertext.data(), (int)ciphertext.size()) != 1) {
        EVP_CIPHER_CTX_free(ctx);
        return false;
    }
    int plain_len = len;

    if (EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_GCM_SET_TAG, tag.size(), (void*)tag.data()) != 1) {
        EVP_CIPHER_CTX_free(ctx);
        return false;
    }

    int ret = EVP_DecryptFinal_ex(ctx, plaintext_out.data() + len, &len);
    EVP_CIPHER_CTX_free(ctx);
    if (ret <= 0) {
        // verification failed
        return false;
    }
    plain_len += len;
    plaintext_out.resize(plain_len);
    return true;
}

// Helper to read file into vector
std::vector<unsigned char> read_file_bytes(const std::string& path) {
    std::ifstream ifs(path, std::ios::binary);
    return std::vector<unsigned char>((std::istreambuf_iterator<char>(ifs)), std::istreambuf_iterator<char>());
}

// Helper to write file
void write_file_bytes(const std::string& path, const std::vector<unsigned char>& data) {
    std::ofstream ofs(path, std::ios::binary);
    ofs.write((const char*)data.data(), data.size());
}

// Example CLI: encrypt / decrypt files
int main(int argc, char** argv) {
    if (argc < 4) {
        std::cerr << "Usage: " << argv[0] << " encrypt|decrypt <keyfile> <infile> <outfile>\n";
        return 2;
    }
    std::string mode = argv[1];
    std::string keyfile = argv[2];
    std::string infile = argv[3];
    std::string outfile = (argc >=5) ? argv[4] : "out.bin";

    auto key_bytes = read_file_bytes(keyfile);
    if (key_bytes.size() < KEY_LEN) {
        std::cerr << "Key file too short. Provide 32 bytes of raw key or use a binary file with 32 bytes." << std::endl;
        return 3;
    }
    std::vector<unsigned char> key(key_bytes.begin(), key_bytes.begin() + KEY_LEN);

    if (mode == "encrypt") {
        auto plaintext = read_file_bytes(infile);
        std::vector<unsigned char> iv, ciphertext, tag;
        if (!aes_gcm_encrypt(key, plaintext, iv, ciphertext, tag)) {
            std::cerr << "Encryption failed" << std::endl;
            return 4;
        }
        // output format: iv || tag || ciphertext
        std::vector<unsigned char> out;
        out.insert(out.end(), iv.begin(), iv.end());
        out.insert(out.end(), tag.begin(), tag.end());
        out.insert(out.end(), ciphertext.begin(), ciphertext.end());
        write_file_bytes(outfile, out);
        std::cout << "Encrypted -> " << outfile << std::endl;
    } else if (mode == "decrypt") {
        auto in = read_file_bytes(infile);
        if (in.size() < IV_LEN + TAG_LEN) {
            std::cerr << "Input file too small to contain iv+tag" << std::endl;
            return 5;
        }
        std::vector<unsigned char> iv(in.begin(), in.begin() + IV_LEN);
        std::vector<unsigned char> tag(in.begin() + IV_LEN, in.begin() + IV_LEN + TAG_LEN);
        std::vector<unsigned char> ciphertext(in.begin() + IV_LEN + TAG_LEN, in.end());
        std::vector<unsigned char> plaintext;
        if (!aes_gcm_decrypt(key, iv, ciphertext, tag, plaintext)) {
            std::cerr << "Decryption failed (auth check)" << std::endl;
            return 6;
        }
        write_file_bytes(outfile, plaintext);
        std::cout << "Decrypted -> " << outfile << std::endl;
    } else {
        std::cerr << "Unknown mode: " << mode << std::endl;
        return 7;
    }
    return 0;
}