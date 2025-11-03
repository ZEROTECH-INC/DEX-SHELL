// checksum_validator.js
// Node.js utility: compute SHA256 of a file, compare to expected value, optional signature verification using RSA public key.

const fs = require('fs');
const crypto = require('crypto');

function sha256file(path) {
  return new Promise((resolve, reject) => {
    const hash = crypto.createHash('sha256');
    const rs = fs.createReadStream(path);
    rs.on('error', reject);
    rs.on('data', (chunk) => hash.update(chunk));
    rs.on('end', () => resolve(hash.digest('hex')));
  });
}

async function main() {
  const args = process.argv.slice(2);
  if (args.length < 2) {
    console.log('Usage: node checksum_validator.js <file> <expected_sha256> [public_key.pem] [signature_file]');
    process.exit(2);
  }
  const [file, expected, pubkeyPath, sigPath] = args;
  try {
    const sum = await sha256file(file);
    console.log('SHA256:', sum);
    if (sum.toLowerCase() === expected.toLowerCase()) {
      console.log('[OK] checksum matches');
    } else {
      console.log('[FAIL] checksum mismatch');
      process.exit(3);
    }

    if (pubkeyPath && sigPath) {
      const pubkey = fs.readFileSync(pubkeyPath, 'utf8');
      const sig = fs.readFileSync(sigPath);
      const verifier = crypto.createVerify('RSA-SHA256');
      const fileBuf = fs.readFileSync(file);
      verifier.update(fileBuf);
      verifier.end();
      const ok = verifier.verify(pubkey, sig);
      console.log(ok ? '[OK] signature valid' : '[FAIL] signature INVALID');
      process.exit(ok ? 0 : 4);
    }
  } catch (e) {
    console.error('Error:', e.message);
    process.exit(1);
  }
}

if (require.main === module) main();