<template>
  <header-component />
  <section v-if="user" class="bg-white shadow sm:rounded-lg" id="about">
    <div class="px-4 py-5 sm:p-6">
      <h2 class="text-3xl my-5 text-center text-red-800">{{ user.username ? user.username : "" }}</h2>
      <div class="flex items-center space-x-4">
        <h3 class="text-lg leading-6 font-medium text-gray-900">
          {{ getFullName(user) }}
        </h3>
        <button v-if="user.followers && user.followers.includes(authData.email) && user.username !== authData.username" @click="unfollowUser"
          class="mt-4 px-4 py-2 ml-2 bg-danger hover:bg-red-900 text-white rounded">
          Unfollow
        </button>
        <button v-else-if="user.username !== authData.username" @click="followUser" class="mt-4 px-4 py-2 ml-2 bg-success hover:bg-green-900 text-white rounded">
          Follow
        </button>
      </div>
      <div class="mt-2 max-w-xl text-sm text-gray-500">
        <p>See the details of this user like questions asked and questions answered.</p>
      </div>

      <div class="mt-8 sm:w-full">
        <div class="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
          <p>
            Number of questions asked: <span class="text-red-800">{{ user.questions ? user.questions.length : 0
              }}</span>
          </p>
          <p>
            Number of questions answered: <span class="text-red-800">{{ user.answers ? user.answers.length : 0 }}</span>
          </p>
          <p class="mt-2">
            Following: <span class="text-red-800">{{ user.following ? user.following.length : 0 }}</span>
          </p>
          <div class="mt-2">
            <span class="text-red-800">
              <span v-for="(follow, index) in user.following" :key="follow.id" class="rounded-lg bg-gray-200 px-2 py-1">
                {{ follow }}<span v-if="index < user.following.length - 1">, </span>
              </span>
            </span>
          </div>
          <p class="mt-2">
            Followers: <span class="text-red-800">{{ user.followers ? user.followers.length : 0 }}</span>
          </p>
          <div class="mt-2">
            <span class="text-red-800">
              <span v-for="(follower, index) in user.followers" :key="follower.id"
                class="rounded-lg bg-gray-200 px-2 py-1">
                {{ follower }}<span v-if="index < user.followers.length - 1">, </span>
              </span>
            </span>
          </div>

          <div>
            <h3 class="text-xl leading-6 font-medium text-primary my-3">
              Questions asked by {{ getFullName(user) }}
            </h3>

            <ul>
              <li v-for="question in user.questions" :key="question.id"
                class="my-2 bg-neutral-100 rounded-lg border-b py-2 border-gray-300">
                <router-link :to="{ name: 'QuestionDetail', params: { slug: question.slug } }">
                  {{ question.content }}
                </router-link>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </section>
  <footer-component />
</template>

<script setup>
import { onMounted, computed } from "vue";
import { useUser } from "../store/user";
import { useAuth } from "../store/auth";
import { useRoute } from "vue-router";

const userStore = useUser();
const route = useRoute();
const authStore = useAuth();

const user = computed(() => userStore.user);
const authData = computed(() => authStore.authData);

const getFullName = (user) => {
  return user.firstName + " " + user.lastName;
};

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
