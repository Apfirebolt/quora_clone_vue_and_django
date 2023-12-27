<script setup>
import { ref } from 'vue'

defineProps({
  msg: String,
})

const count = ref(0)
</script>

<template>
  <h1>{{ msg }} Hi Message King</h1>

  <div class="card">
    <button type="button" @click="count++">count is {{ count }}</button>
    <p class="text-red-500">
      Edit This Man
      <code>components/HelloWorld.vue</code> to test HMR
    </p>
  </div>
</template>

<style scoped>
.read-the-docs {
  color: #888;
}
</style>
