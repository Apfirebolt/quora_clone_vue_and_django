<template>
  <header-component />

  <main class="min-h-[calc(100vh-4rem)] bg-neutral/10 py-10 px-4 sm:px-6 lg:px-8 font-inter" id="about">
    <div class="mx-auto max-w-5xl space-y-8">
      
      <!-- Top Profile Overview Hero Card -->
      <section class="relative overflow-hidden rounded-3xl border border-gray-100 bg-white p-6 sm:p-8 shadow-sm">
        <div class="pointer-events-none absolute -top-16 right-0 h-44 w-44 rounded-full bg-blue-100/50 blur-3xl"></div>

        <div class="relative flex flex-col sm:flex-row items-center sm:items-start justify-between gap-6">
          <div class="flex flex-col sm:flex-row items-center gap-5 text-center sm:text-left">
            
            <!-- Avatar with Quick Action Trigger -->
            <div class="relative group">
              <img
                v-if="profileData && profileData.profilePicture"
                :src="completeImageUrl"
                alt="Profile Avatar"
                class="h-24 w-24 rounded-3xl object-cover ring-4 ring-slate-100 shadow-md transition group-hover:opacity-90"
              />
              <div
                v-else
                class="flex h-24 w-24 items-center justify-center rounded-3xl bg-gradient-to-br from-primary to-secondary text-2xl font-bold text-accent ring-4 ring-slate-100 shadow-md"
              >
                {{ (username || email || 'U').charAt(0).toUpperCase() }}
              </div>

              <!-- Overlay Camera Trigger -->
              <button
                @click="openModal"
                type="button"
                class="absolute -bottom-2 -right-2 flex h-8 w-8 items-center justify-center rounded-xl bg-slate-900 text-white shadow-md transition-transform hover:scale-110 hover:bg-primary focus:outline-none"
                title="Change Avatar"
              >
                <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
              </button>
            </div>

            <!-- Profile Identifiers -->
            <div class="space-y-1">
              <div class="flex items-center justify-center sm:justify-start gap-2">
                <h1 class="text-xl sm:text-2xl font-bold tracking-tight text-slate-900">
                  {{ firstName || lastName ? `${firstName} ${lastName}` : username }}
                </h1>
                <span class="inline-flex items-center rounded-md bg-blue-50 px-2 py-0.5 text-xs font-semibold text-blue-700 ring-1 ring-inset ring-blue-700/10">
                  Active
                </span>
              </div>
              <p class="text-xs sm:text-sm text-slate-500 font-medium">@{{ username }}</p>
              <p class="text-xs text-slate-400">{{ email }}</p>
            </div>
          </div>

          <!-- Direct Upload Button -->
          <button
            @click="openModal"
            type="button"
            class="inline-flex items-center gap-2 rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-xs font-semibold text-slate-700 shadow-2xs transition hover:bg-slate-50 hover:border-slate-300 focus:outline-none focus:ring-2 focus:ring-primary/20 active:scale-[0.98]"
          >
            <svg class="h-4 w-4 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            <span>Update Photo</span>
          </button>
        </div>
      </section>

      <Loader v-if="isLoading" />

      <!-- Form Grid -->
      <div v-else class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        
        <!-- Account Info Form -->
        <div class="rounded-3xl border border-slate-200/80 bg-white p-6 sm:p-8 shadow-sm flex flex-col justify-between">
          <div class="space-y-6">
            <div class="border-b border-slate-100 pb-4">
              <h2 class="text-lg font-bold tracking-tight text-slate-900">Personal Details</h2>
              <p class="text-xs text-slate-400 mt-0.5">Manage your public information and identity</p>
            </div>

            <form class="space-y-4" @submit.prevent="handleSubmit">
              <div class="grid sm:grid-cols-2 gap-4">
                <div class="space-y-1.5">
                  <label for="firstName" class="block text-xs font-bold uppercase tracking-wider text-slate-700">First Name</label>
                  <input
                    id="firstName"
                    name="firstName"
                    v-model="firstName"
                    type="text"
                    placeholder="John"
                    class="w-full rounded-xl border border-slate-200 bg-slate-50/60 px-4 py-2.5 text-sm text-slate-900 placeholder-slate-400 transition focus:bg-white focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20"
                  />
                </div>
                <div class="space-y-1.5">
                  <label for="lastName" class="block text-xs font-bold uppercase tracking-wider text-slate-700">Last Name</label>
                  <input
                    id="lastName"
                    name="lastName"
                    v-model="lastName"
                    type="text"
                    placeholder="Doe"
                    class="w-full rounded-xl border border-slate-200 bg-slate-50/60 px-4 py-2.5 text-sm text-slate-900 placeholder-slate-400 transition focus:bg-white focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20"
                  />
                </div>
              </div>

              <div class="space-y-1.5">
                <label for="username" class="block text-xs font-bold uppercase tracking-wider text-slate-700">Username</label>
                <div class="relative">
                  <span class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3.5 text-slate-400 text-sm font-semibold">@</span>
                  <input
                    id="username"
                    name="username"
                    v-model="username"
                    type="text"
                    required
                    placeholder="username"
                    class="w-full rounded-xl border border-slate-200 bg-slate-50/60 py-2.5 pl-8 pr-4 text-sm text-slate-900 placeholder-slate-400 transition focus:bg-white focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20"
                  />
                </div>
              </div>

              <div class="space-y-1.5">
                <label for="email" class="block text-xs font-bold uppercase tracking-wider text-slate-700">Email Address</label>
                <div class="relative">
                  <span class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3.5 text-slate-400">
                    <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.206" />
                    </svg>
                  </span>
                  <input
                    id="email"
                    name="email"
                    v-model="email"
                    type="email"
                    required
                    placeholder="name@example.com"
                    class="w-full rounded-xl border border-slate-200 bg-slate-50/60 py-2.5 pl-10 pr-4 text-sm text-slate-900 placeholder-slate-400 transition focus:bg-white focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20"
                  />
                </div>
              </div>

              <div class="pt-3 border-t border-slate-100">
                <button
                  type="submit"
                  class="inline-flex w-full sm:w-auto items-center justify-center gap-2 rounded-xl bg-primary px-5 py-2.5 text-sm font-semibold text-accent shadow-sm transition hover:bg-secondary focus:outline-none focus:ring-2 focus:ring-primary/40 active:scale-[0.98]"
                >
                  <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                  </svg>
                  <span>Save Changes</span>
                </button>
              </div>
            </form>
          </div>
        </div>

        <!-- Security / Password Change Form -->
        <div class="rounded-3xl border border-slate-200/80 bg-white p-6 sm:p-8 shadow-sm flex flex-col justify-between">
          <div class="space-y-6">
            <div class="border-b border-slate-100 pb-4">
              <h2 class="text-lg font-bold tracking-tight text-slate-900">Security & Credentials</h2>
              <p class="text-xs text-slate-400 mt-0.5">Ensure your account is protected with a secure password</p>
            </div>

            <form class="space-y-4" @submit.prevent="handlePasswordChange">
              <div class="space-y-1.5">
                <label for="current_password" class="block text-xs font-bold uppercase tracking-wider text-slate-700">Current Password</label>
                <div class="relative">
                  <span class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3.5 text-slate-400">
                    <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                    </svg>
                  </span>
                  <input
                    id="current_password"
                    name="current_password"
                    v-model="current_password"
                    type="password"
                    required
                    placeholder="••••••••"
                    class="w-full rounded-xl border border-slate-200 bg-slate-50/60 py-2.5 pl-10 pr-4 text-sm text-slate-900 placeholder-slate-400 transition focus:bg-white focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20"
                  />
                </div>
              </div>

              <div class="space-y-1.5">
                <label for="new_password" class="block text-xs font-bold uppercase tracking-wider text-slate-700">New Password</label>
                <div class="relative">
                  <span class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3.5 text-slate-400">
                    <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
                    </svg>
                  </span>
                  <input
                    id="new_password"
                    name="new_password"
                    v-model="new_password"
                    type="password"
                    required
                    placeholder="••••••••"
                    class="w-full rounded-xl border border-slate-200 bg-slate-50/60 py-2.5 pl-10 pr-4 text-sm text-slate-900 placeholder-slate-400 transition focus:bg-white focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20"
                  />
                </div>
              </div>

              <div class="pt-3 border-t border-slate-100">
                <button
                  type="submit"
                  class="inline-flex w-full sm:w-auto items-center justify-center gap-2 rounded-xl bg-slate-900 px-5 py-2.5 text-sm font-semibold text-white shadow-sm transition hover:bg-primary focus:outline-none focus:ring-2 focus:ring-primary/40 active:scale-[0.98]"
                >
                  <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                  </svg>
                  <span>Update Password</span>
                </button>
              </div>
            </form>
          </div>
        </div>

      </div>

    </div>

    <!-- Update Profile Image Modal -->
    <TransitionRoot appear :show="isUpdateProfileImageModalOpen" as="template">
      <Dialog as="div" @close="closeModal" class="relative z-50">
        <TransitionChild
          as="template"
          enter="duration-300 ease-out"
          enter-from="opacity-0"
          enter-to="opacity-100"
          leave="duration-200 ease-in"
          leave-from="opacity-100"
          leave-to="opacity-0"
        >
          <div class="fixed inset-0 bg-neutral-950/60 backdrop-blur-xs" />
        </TransitionChild>

        <div class="fixed inset-0 overflow-y-auto">
          <div class="flex min-h-full items-center justify-center p-4 text-center">
            <TransitionChild
              as="template"
              enter="duration-300 ease-out"
              enter-from="opacity-0 scale-95"
              enter-to="opacity-100 scale-100"
              leave="duration-200 ease-in"
              leave-from="opacity-100 scale-100"
              leave-to="opacity-0 scale-95"
            >
              <DialogPanel class="w-full max-w-md transform overflow-hidden rounded-3xl bg-white p-6 sm:p-8 text-left align-middle shadow-2xl border border-slate-100 transition-all">
                <ChangeProfilePicture
                  :closeModal="closeModal"
                  :updateProfileImage="updateProfilePictureUtil"
                />
              </DialogPanel>
            </TransitionChild>
          </div>
        </div>
      </Dialog>
    </TransitionRoot>
  </main>

  <footer-component />
</template>

<script setup>
import { ref, onMounted, computed, watch } from "vue";
import { useAuth } from "../store/auth";
import FooterComponent from "../components/FooterComponent.vue";
import ChangeProfilePicture from "../components/ChangeProfilePicture.vue";
import Loader from "../components/Loader.vue";
import {
  TransitionRoot,
  TransitionChild,
  Dialog,
  DialogPanel,
} from "@headlessui/vue";

const authStore = useAuth();

const email = ref("");
const username = ref("");
const firstName = ref("");
const lastName = ref("");
const current_password = ref("");
const new_password = ref("");
const isUpdateProfileImageModalOpen = ref(false);

const profileData = computed(() => authStore.getProfileData);
const isLoading = computed(() => authStore.isLoading);

const completeImageUrl = computed(() => {
  if (profileData.value && profileData.value.profilePicture) {
    return `http://localhost:8000${profileData.value.profilePicture}`;
  }
  return "";
});

const closeModal = () => {
  isUpdateProfileImageModalOpen.value = false;
};

const openModal = () => {
  isUpdateProfileImageModalOpen.value = true;
};

watch(
  profileData,
  (newVal) => {
    if (newVal) {
      email.value = newVal.email || "";
      username.value = newVal.username || "";
      firstName.value = newVal.firstName || "";
      lastName.value = newVal.lastName || "";
    }
  },
  { immediate: true }
);

const updateProfilePictureUtil = async (formData) => {
  await authStore.changeProfileImage(formData);
  closeModal();
  await authStore.getProfileDataAction();
};

const handleSubmit = async () => {
  const payload = {
    id: profileData.value?.id,
    email: email.value,
    username: username.value,
    firstName: firstName.value,
    lastName: lastName.value,
  };
  await authStore.updateProfileDataAction(payload);
};

const handlePasswordChange = async () => {
  const payload = {
    current_password: current_password.value,
    new_password: new_password.value,
  };
  await authStore.changePassword(payload);
  current_password.value = "";
  new_password.value = "";
};

onMounted(async () => {
  await authStore.getProfileDataAction();
});
</script>