<template>
  <header-component />
  <section v-if="user" class="bg-white shadow sm:rounded-lg" id="about">
    <div class="px-4 py-5 sm:p-6">
      <h2 class="text-3xl my-5 text-center text-red-800">{{ user.username ? user.username : "" }}</h2>
      <h3 class="text-lg leading-6 font-medium text-gray-900">
        {{ getFullName(user) }}
      </h3>
      <div class="mt-2 max-w-xl text-sm text-gray-500">
        <p>See the details of this user like questions asked and questions answered.</p>
      </div>

      <div class="mt-8 sm:w-full">
        <div class="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
          <p>
            Number of questions asked: <span class="text-red-800">{{ user.questions ? user.questions.length : 0 }}</span>
          </p>
          <p>
            Number of questions answered: <span class="text-red-800">{{ user.answers ? user.answers.length : 0 }}</span>
          </p>

          <div>
            <h3 class="text-xl leading-6 font-medium text-primary my-3">
              Questions asked by {{ getFullName(user) }}
            </h3>

            <ul>
                <li v-for="question in user.questions" :key="question.id" class="my-2 bg-neutral-100 rounded-lg border-b py-2 border-gray-300">
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
import { useRoute } from "vue-router";

const userStore = useUser();
const route = useRoute();

const user = computed(() => userStore.user);

const getFullName = (user) => {
  return user.firstName + " " + user.lastName;
};

onMounted(async () => {
  const username = route.params.username;  
  await userStore.getUserAction(username);
});
</script>
