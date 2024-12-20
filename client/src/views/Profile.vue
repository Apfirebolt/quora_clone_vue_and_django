<template>
  <header-component />
  <section class="bg-white shadow sm:rounded-lg" id="about">
    <div class="px-4 py-5 sm:p-6">
      <h2 class="text-3xl my-5 text-center text-red-800">PROFILE</h2>
      <h3 class="text-lg leading-6 font-medium text-gray-900">
        Update your profile
      </h3>
      <div class="mt-2 max-w-xl text-sm text-gray-500">
        <p>Change the email address you want associated with your account.</p>
      </div>
      
      <div class="mt-8 flex w-full">
        <div class="bg-white py-8 w-1/2 px-4 shadow sm:rounded-lg sm:px-10">
          <form class="space-y-6" @submit="handleSubmit">
            <div>
              <label
                for="email"
                class="block text-sm font-medium text-gray-700"
              >
                Email address
              </label>
              <div class="mt-1">
                <input
                  id="email"
                  name="email"
                  v-model="email"
                  type="email"
                  required=""
                  placeholder="Enter Email"
                  class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                />
              </div>
            </div>

            <div>
              <label
                for="username"
                class="block text-sm font-medium text-gray-700"
              >
                Username
              </label>
              <div class="mt-1">
                <input
                  id="username"
                  name="username"
                  v-model="username"
                  type="text"
                  required=""
                  placeholder="Enter Username"
                  class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                />
              </div>
            </div>

            <div class="grid md:grid-cols-2 gap-4">
              <div>
                <label
                  for="firstName"
                  class="block text-sm font-medium text-gray-700"
                >
                  First Name
                </label>
                <div class="mt-1">
                  <input
                    id="firstName"
                    name="firstName"
                    v-model="firstName"
                    type="text"
                    placeholder="Enter First Name"
                    class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  />
                </div>
              </div>

              <div>
                <label
                  for="lastName"
                  class="block text-sm font-medium text-gray-700"
                >
                  Last Name
                </label>
                <div class="mt-1">
                  <input
                    id="lastName"
                    name="lastName"
                    v-model="lastName"
                    type="text"
                    placeholder="Enter Last Name"
                    class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  />
                </div>
              </div>
            </div>

            <div class="text-center">
              <button
                type="submit"
                class="py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-secondary hover:bg-primary focus:outline-none focus:ring-2 focus:ring-offset-2"
              >
                Update Profile
              </button>
            </div>
          </form>
        </div>
        <div class="bg-white py-8 w-1/2 px-4 shadow sm:rounded-lg sm:px-10">
          <form class="space-y-6" @submit="handlePasswordChange">
            <div>
              <label
                for="current_password"
                class="block text-sm font-medium text-gray-700"
              >
                Current Password
              </label>
              <div class="mt-1">
                <input
                  id="current_password"
                  name="current_password"
                  v-model="current_password"
                  type="password"
                  required=""
                  placeholder="Enter Current Password"
                  class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                />
              </div>
            </div>

            <div>
              <label
                for="new_password"
                class="block text-sm font-medium text-gray-700"
              >
                New Password
              </label>
              <div class="mt-1">
                <input
                  id="new_password"
                  name="new_password"
                  v-model="new_password"
                  type="password"
                  required=""
                  placeholder="Enter New Password"
                  class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                />
              </div>
            </div>

            <div class="text-center">
              <button
                type="submit"
                class="py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-secondary hover:bg-primary focus:outline-none focus:ring-2 focus:ring-offset-2"
              >
                Update Password
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </section>
  <footer-component />
</template>

<script setup>
import { ref, onMounted, computed, watch } from "vue";
import { useAuth } from "../store/auth";
import router from "../routes/index";
import FooterComponent from "../components/FooterComponent.vue";

const authStore = useAuth();

const email = ref("");
const username = ref("");
const firstName = ref("");
const lastName = ref("");
const current_password = ref("");
const new_password = ref("");

const profileData = computed(() => authStore.getProfileData);

// if profileData is not null and is changed then update values
watch(profileData, (newVal) => {
  if (newVal) {
    email.value = newVal.email;
    username.value = newVal.username;
    firstName.value = newVal.firstName;
    lastName.value = newVal.lastName;
  }
});

const handleSubmit = async (e) => {
  e.preventDefault();
  let payload = {
    id: profileData.value.id,
    email: email.value,
    username: username.value,
    firstName: firstName.value,
    lastName: lastName.value,
  };
  await authStore.updateProfileDataAction(payload);
};

const handlePasswordChange = async (e) => {
  e.preventDefault();
  let payload = {
    current_password: current_password.value,
    new_password: new_password.value,
  };
  await authStore.changePassword(payload);
};

onMounted(async () => {
  await authStore.getProfileDataAction();
});
</script>
