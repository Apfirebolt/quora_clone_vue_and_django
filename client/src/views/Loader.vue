<template>
    <div class="flex items-center justify-center min-h-screen">
        <div class="loader ease-linear rounded-full border-8 border-t-8 border-gray-200 h-64 w-64"></div>
    </div>
</template>

<script>
export default {
    name: 'Loader'
}
</script>

<style scoped>
.loader {
    border-top-color: #3490dc;
    animation: spin 1.5s linear infinite;
}

@keyframes spin {
    0% {
        transform: rotate(0deg);
    }
    100% {
        transform: rotate(360deg);
    }
}
</style>