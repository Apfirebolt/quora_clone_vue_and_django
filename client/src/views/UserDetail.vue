<template>
  <header-component />
  <main v-if="user" class="bg-white shadow sm:rounded-lg" id="about">
    <section class="px-4 py-5 sm:p-6 container mx-auto">
      <div class="flex justify-around items-center bg-accent pt-2 rounded-lg">
        <section-header
          :title="getFullName(user)"
          subtitle="See the details of this user like questions asked and questions answered."
        />
      </div>

      <Loader v-if="isLoading" />

      <div v-else class="mt-8 sm:w-full">
        <div
          class="bg-gradient-to-br from-white to-gray-50 py-8 px-6 shadow-lg rounded-xl border border-gray-100"
        >
          <!-- Follow or Unfollow Button -->
          <button
            v-if="
              user.followers &&
              user.followers.includes(authData.email) &&
              user.username !== authData.username
            "
            @click="unfollowUser"
            class="px-4 py-2 mb-2 bg-danger hover:bg-red-900 text-white rounded"
          >
            Unfollow
          </button>
          <button
            v-else-if="user.username !== authData.username"
            @click="followUser"
            class="px-4 py-2 mb-2 bg-success hover:bg-green-900 text-white rounded"
          >
            Follow
          </button>
          <!-- Stats Grid -->
          <div class="grid grid-cols-2 gap-6 mb-8">
            <div
              class="bg-white p-4 rounded-lg shadow-sm border border-gray-100"
            >
              <div class="text-sm font-medium text-gray-600">
                Questions Asked
              </div>
              <div class="text-2xl font-bold text-blue-600">
                {{ user.questions ? user.questions.length : 0 }}
              </div>
            </div>
            <div
              class="bg-white p-4 rounded-lg shadow-sm border border-gray-100"
            >
              <div class="text-sm font-medium text-gray-600">
                Questions Answered
              </div>
              <div class="text-2xl font-bold text-green-600">
                {{ user.answers ? user.answers.length : 0 }}
              </div>
            </div>
          </div>

          <!-- Following Section -->
          <div class="mb-6">
            <div class="flex items-center mb-3">
              <h4 class="text-lg font-semibold text-gray-800">Following</h4>
              <span
                class="ml-2 px-2 py-1 text-xs font-medium bg-blue-100 text-blue-800 rounded-full"
              >
                {{ user.following ? user.following.length : 0 }}
              </span>
            </div>
            <div class="flex flex-wrap gap-2">
              <span
                v-for="follow in user.following"
                :key="follow.id"
                class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-50 text-blue-700 border border-blue-200 hover:bg-blue-100 transition-colors duration-200"
              >
                {{ follow }}
              </span>
            </div>
          </div>

          <!-- Followers Section -->
          <div class="mb-8">
            <div class="flex items-center mb-3">
              <h4 class="text-lg font-semibold text-gray-800">Followers</h4>
              <span
                class="ml-2 px-2 py-1 text-xs font-medium bg-green-100 text-green-800 rounded-full"
              >
                {{ user.followers ? user.followers.length : 0 }}
              </span>
            </div>
            <div class="flex flex-wrap gap-2">
              <span
                v-for="follower in user.followers"
                :key="follower.id"
                class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-50 text-green-700 border border-green-200 hover:bg-green-100 transition-colors duration-200"
              >
                {{ follower }}
              </span>
            </div>
          </div>

          <!-- Questions Section -->
          <div class="border-t border-gray-200 pt-6">
            <h3 class="text-xl font-bold text-gray-800 mb-4 flex items-center">
              <svg
                class="w-5 h-5 mr-2 text-blue-600"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path
                  fill-rule="evenodd"
                  d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-8-3a1 1 0 00-.867.5 1 1 0 11-1.731-1A3 3 0 0113 8a3.001 3.001 0 01-2 2.83V11a1 1 0 11-2 0v-1a1 1 0 011-1 1 1 0 100-2zm0 8a1 1 0 100-2 1 1 0 000 2z"
                  clip-rule="evenodd"
                ></path>
              </svg>
              Questions asked by {{ getFullName(user) }}
            </h3>

            <div class="space-y-3">
              <div
                v-for="question in user.questions"
                :key="question.id"
                class="group"
              >
                <router-link
                  :to="{
                    name: 'QuestionDetail',
                    params: { slug: question.slug },
                  }"
                  class="block p-4 bg-white rounded-lg border border-gray-200 hover:border-blue-300 hover:shadow-md transition-all duration-200 group-hover:bg-blue-50"
                >
                  <p
                    class="text-gray-800 group-hover:text-blue-800 font-medium"
                  >
                    {{ question.content }}
                  </p>
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </main>
  <footer-component />
</template>

<script setup>
import { onMounted, computed } from "vue";
import { useUser } from "../store/user";
import { useAuth } from "../store/auth";
import { useRoute } from "vue-router";
import Loader from "../components/Loader.vue";
import SectionHeader from "../components/SectionHeader.vue";

const userStore = useUser();
const route = useRoute();
const authStore = useAuth();

const user = computed(() => userStore.user);
const authData = computed(() => authStore.authData);

const getFullName = (user) => {
  return user.firstName + " " + user.lastName;
};

const isLoading = computed(() => userStore.isLoading);

async function followUser() {
  await userStore.followUserAction(user.value.username);
  await userStore.getUserAction(user.value.username);
}

async function unfollowUser() {
  await userStore.unfollowUserAction(user.value.username);
  await userStore.getUserAction(user.value.username);
}

onMounted(async () => {
  const username = route.params.username;
  await userStore.getUserAction(username);
});
</script>
