<template>
  <div class="min-h-[calc(100vh-4rem)] bg-neutral/10 flex flex-col justify-center py-12 px-4 sm:px-6 lg:px-8 font-inter">
    <div class="sm:mx-auto sm:w-full sm:max-w-md">
      
      <!-- Brand & Title Header -->
      <div class="text-center space-y-3">
        <router-link to="/" class="inline-flex items-center justify-center">
          <img v-if="logo" class="h-12 w-12 rounded-2xl shadow-sm ring-4 ring-white object-cover" :src="logo" alt="Logo" />
          <div v-else class="flex h-12 w-12 items-center justify-center rounded-2xl bg-primary text-accent text-xl font-bold shadow-md shadow-primary/20">
            Q
          </div>
        </router-link>

        <h1 class="text-2xl sm:text-3xl font-bold tracking-tight text-secondary">
          Welcome back
        </h1>
        <p class="text-xs sm:text-sm text-slate-500">
          Enter your credentials to access your account
        </p>
      </div>

      <!-- Auth Card -->
      <div class="mt-8">
        <div class="relative overflow-hidden rounded-3xl bg-white p-6 sm:p-8 shadow-xl border border-slate-100">
          <!-- Subtle Accent Ambient Glow -->
          <div class="pointer-events-none absolute -top-16 right-0 h-40 w-40 rounded-full bg-primary/10 blur-3xl"></div>

          <form class="relative space-y-5" @submit.prevent="onSubmit">
            
            <!-- Email Input -->
            <div class="space-y-1.5">
              <label for="email" class="block text-xs font-bold uppercase tracking-wider text-slate-700">
                Email address
              </label>
              <div class="relative">
                <span class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3.5 text-slate-400">
                  <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.206" />
                  </svg>
                </span>
                <input
                  id="email"
                  v-bind="email"
                  name="email"
                  type="email"
                  placeholder="name@example.com"
                  autocomplete="email"
                  class="w-full rounded-xl border bg-slate-50/60 py-2.5 pl-10 pr-4 text-sm text-slate-900 placeholder-slate-400 transition focus:bg-white focus:outline-none focus:ring-2"
                  :class="errors.email ? 'border-rose-400 focus:border-rose-500 focus:ring-rose-500/20' : 'border-slate-200 focus:border-primary focus:ring-primary/20'"
                />
              </div>
              <p v-if="errors.email" class="text-xs font-medium text-rose-600">
                {{ errors.email }}
              </p>
            </div>

            <!-- Password Input -->
            <div class="space-y-1.5">
              <div class="flex items-center justify-between">
                <label for="password" class="block text-xs font-bold uppercase tracking-wider text-slate-700">
                  Password
                </label>
              </div>
              <div class="relative">
                <span class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3.5 text-slate-400">
                  <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                  </svg>
                </span>
                <input
                  id="password"
                  v-bind="password"
                  name="password"
                  type="password"
                  placeholder="••••••••"
                  autocomplete="current-password"
                  class="w-full rounded-xl border bg-slate-50/60 py-2.5 pl-10 pr-4 text-sm text-slate-900 placeholder-slate-400 transition focus:bg-white focus:outline-none focus:ring-2"
                  :class="errors.password ? 'border-rose-400 focus:border-rose-500 focus:ring-rose-500/20' : 'border-slate-200 focus:border-primary focus:ring-primary/20'"
                />
              </div>
              <p v-if="errors.password" class="text-xs font-medium text-rose-600">
                {{ errors.password }}
              </p>
            </div>

            <!-- Submit Action -->
            <div class="pt-2">
              <button
                type="submit"
                class="inline-flex w-full items-center justify-center gap-2 rounded-xl bg-primary px-4 py-3 text-sm font-semibold text-accent shadow-sm transition-all hover:bg-secondary focus:outline-none focus:ring-2 focus:ring-primary/40 active:scale-[0.98]"
              >
                <span>Sign in</span>
                <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
                </svg>
              </button>
            </div>

            <!-- Register Alternative -->
            <div class="pt-2 text-center border-t border-slate-100">
              <p class="text-xs text-slate-500">
                Don't have an account?
                <router-link
                  to="/register"
                  class="font-semibold text-primary hover:text-secondary transition-colors ml-1"
                >
                  Create one now
                </router-link>
              </p>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
  <FooterComponent />
</template>

<script setup>
import { computed } from "vue";
import { useAuth } from "../store/auth";
import { useForm } from "vee-validate";
import router from "../routes/index";
import FooterComponent from "../components/FooterComponent.vue";
import logo from "../assets/1.png";

const auth = useAuth();
const authData = computed(() => auth.getAuthData);

// Validation rules
function required(value) {
  return value ? true : "Email is required";
}

function passwordRequired(value) {
  if (!value) {
    return "Password is required";
  }
  if (value.length < 8) {
    return "Password must be at least 8 characters";
  }
  return true;
}

// Create form
const { defineInputBinds, handleSubmit, errors } = useForm({
  validationSchema: {
    email: required,
    password: passwordRequired,
  },
});

// Define fields
const email = defineInputBinds("email");
const password = defineInputBinds("password");

// Submit handler
const onSubmit = handleSubmit(async (values) => {
  await auth.loginAction(values);
});
</script>