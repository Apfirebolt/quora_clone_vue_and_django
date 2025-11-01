<template>
  <div class="text-center mb-8">
    <h2 class="text-4xl font-bold text-gray-800 mb-2">
      {{ title }}
    </h2>
    <div
      class="w-24 h-1 bg-gradient-to-r from-blue-500 to-purple-600 mx-auto rounded-full"
    ></div>
    <h3 class="text-lg leading-6 font-medium text-gray-900 my-3">
      {{ subtitle }}
    </h3>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
const props = defineProps({
  title: {
    type: String,
    required: true,
  },
  subtitle: {
    type: String,
    required: false,
    default: "",
  },
});
</script>
