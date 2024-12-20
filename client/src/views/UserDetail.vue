<template>
  <header-component />
  <section class="bg-white shadow sm:rounded-lg" id="about">
    <div class="px-4 py-5 sm:p-6">
      <h2 class="text-3xl my-5 text-center text-red-800">{{ user.username ? user.username : "" }}</h2>
      <h3 class="text-lg leading-6 font-medium text-gray-900">
        Update your profile
      </h3>
      <div class="mt-2 max-w-xl text-sm text-gray-500">
        <p>See the details of this user like questions asked and questions answered.</p>
      </div>

      <div class="mt-8 sm:w-full">
        <div class="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
          {{ user }}
        </div>
      </div>
    </div>
  </section>
  <footer-component />
</template>

<script setup>
import { onMounted, computed } from "vue";
import { useUser } from "../store/user";
import { useRoute } from "vue-router";

const userStore = useUser();
const route = useRoute();

const user = computed(() => userStore.user);

onMounted(async () => {
  const username = route.params.username;  
  await userStore.getUserAction(username);
});
</script>
