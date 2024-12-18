<template>
    <header-component />
    <section class="bg-white shadow sm:rounded-lg" id="about">
        <div class="px-4 py-5 sm:p-6">
            <h2 class="text-3xl my-5 text-center text-red-800">PEOPLE</h2>
            <div>
                <h3 class="text-lg leading-6 font-medium text-gray-900">
                    Connect with other users through questions and answers.
                </h3>
            </div>

            <div class="mt-5">
                <ul class="divide-y divide-gray-200">
                    <li v-for="user in users" :key="user.id" class="py-4">
                        <div class="flex space-x-3">
                            <div class="flex-1 space-y-1">
                                <p class="text-sm font-medium text-gray-900">
                                    {{ user.email }}
                                </p>
                                <p class="text-sm text-gray-500">
                                    {{ user.username }}
                                </p>
                            </div>
                            <div>
                                <button
                                    class="text-green-600 hover:text-green-900 mx-2 px-2 py-1 rounded-md shadow-lg">View</button>
                            </div>
                        </div>
                    </li>
                </ul>
            </div>
        </div>
    </section>
    <footer-component />
</template>

<script setup>
import { onMounted, computed } from 'vue';
import { useUser } from "../store/user";

const userStore = useUser();

const users = computed(() => userStore.getUsers);

onMounted(async () => {
    await userStore.getUsersAction();
});
</script>