#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MEMORY_POOL_SIZE 1024 * 1024 // 1 MB pool

static unsigned char memory_pool[MEMORY_POOL_SIZE];
static size_t used_memory = 0;

void* dex_malloc(size_t size) {
    if (used_memory + size > MEMORY_POOL_SIZE) {
        printf("[MemoryManager] Out of memory!\n");
        return NULL;
    }
    void* ptr = memory_pool + used_memory;
    used_memory += size;
    printf("[MemoryManager] Allocated %zu bytes (Used: %zu/%d)\n", size, used_memory, MEMORY_POOL_SIZE);
    return ptr;
}

void dex_free_all() {
    used_memory = 0;
    printf("[MemoryManager] Memory reset.\n");
}

void dex_memory_status() {
    printf("[MemoryManager] Used: %zu bytes / %d total\n", used_memory, MEMORY_POOL_SIZE);
}