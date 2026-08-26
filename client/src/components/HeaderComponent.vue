<template>
  <Disclosure as="nav" class="sticky top-0 z-50 bg-neutral/95 backdrop-blur-md border-b border-neutral-800 font-inter text-primary" v-slot="{ open }">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="relative flex items-center justify-between h-16">
        
        <!-- Mobile menu toggle button -->
        <div class="absolute inset-y-0 left-0 flex items-center sm:hidden">
          <DisclosureButton
            class="inline-flex items-center justify-center p-2 rounded-xl text-neutral-400 hover:text-white hover:bg-neutral-800/80 focus:outline-none focus:ring-2 focus:ring-primary"
          >
            <span class="sr-only">Open main menu</span>
            <MenuIcon v-if="!open" class="block h-5 w-5" aria-hidden="true" />
            <XIcon v-else class="block h-5 w-5" aria-hidden="true" />
          </DisclosureButton>
        </div>

        <!-- Left: Brand Logo & Main Navigation -->
        <div class="flex-1 flex items-center justify-center sm:items-stretch sm:justify-start">
          <!-- Logo -->
          <router-link :to="{ name: 'Home' }" class="flex-shrink-0 flex items-center gap-2.5 group">
            <img v-if="logo" :src="logo" alt="Logo" class="h-8 w-8 rounded-xl object-cover shadow-sm ring-1 ring-white/10" />
            <div v-else class="flex h-8 w-8 items-center justify-center rounded-xl bg-primary font-bold text-white text-base shadow-sm">
              Q
            </div>
            <span class="hidden md:inline-block font-bold tracking-tight text-white group-hover:text-neutral-200 transition-colors">
              Quora Clone
            </span>
          </router-link>

          <!-- Desktop Navigation links -->
          <div class="hidden sm:flex sm:items-center sm:ml-8">
            <div class="flex items-center space-x-1">
              <!-- Authenticated Nav Items -->
              <template v-if="authData">
                <router-link
                  v-for="item in authMenu"
                  :key="item.name"
                  :to="{ name: item.name }"
                  :class="[
                    isCurrentRoute(item.name)
                      ? 'bg-neutral-800 text-white font-semibold shadow-xs'
                      : 'text-neutral-300 hover:bg-neutral-800/60 hover:text-white font-medium',
                    'px-3.5 py-2 rounded-xl text-xs lg:text-sm transition-all duration-150',
                  ]"
                  :aria-current="isCurrentRoute(item.name) ? 'page' : undefined"
                >
                  {{ item.path }}
                </router-link>
              </template>

              <!-- Guest Nav Items -->
              <template v-else>
                <router-link
                  v-for="item in navigation"
                  :key="item.name"
                  :to="{ name: item.name }"
                  :class="[
                    isCurrentRoute(item.name)
                      ? 'bg-neutral-800 text-white font-semibold'
                      : 'text-neutral-300 hover:bg-neutral-800/60 hover:text-white font-medium',
                    'px-3.5 py-2 rounded-xl text-sm transition-all duration-150',
                  ]"
                  :aria-current="isCurrentRoute(item.name) ? 'page' : undefined"
                >
                  {{ item.name }}
                </router-link>
              </template>
            </div>
          </div>
        </div>

        <!-- Right: Actions & User Dropdown Profile Menu -->
        <div class="absolute inset-y-0 right-0 flex items-center pr-2 sm:static sm:inset-auto sm:ml-6 sm:pr-0">
          <Menu v-if="authData" as="div" class="relative ml-3">
            <div>
              <MenuButton
                class="flex items-center gap-2.5 rounded-full p-1 pr-3 bg-neutral-900 border border-neutral-800 hover:border-neutral-700 hover:bg-neutral-850 transition-all focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2 focus:ring-offset-neutral"
              >
                <!-- Avatar Pill -->
                <div class="flex h-7 w-7 items-center justify-center rounded-full bg-gradient-to-br from-primary to-secondary text-xs font-bold text-accent shadow-xs">
                  {{ (authData.username || authData.email || 'U').charAt(0).toUpperCase() }}
                </div>
                <span class="hidden md:inline-block text-xs font-medium text-neutral-200 truncate max-w-[120px]">
                  {{ authData.username || authData.email }}
                </span>
                <svg class="h-3.5 w-3.5 text-neutral-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </MenuButton>
            </div>

            <transition
              enter-active-class="transition ease-out duration-150"
              enter-from-class="transform opacity-0 scale-95 -translate-y-1"
              enter-to-class="transform opacity-100 scale-100 translate-y-0"
              leave-active-class="transition ease-in duration-100"
              leave-from-class="transform opacity-100 scale-100 translate-y-0"
              leave-to-class="transform opacity-0 scale-95 -translate-y-1"
            >
              <MenuItems
                class="origin-top-right absolute right-0 mt-2 w-56 rounded-2xl bg-white p-1.5 shadow-xl ring-1 ring-black/5 focus:outline-none z-50 border border-slate-100"
              >
                <!-- User identifier label in popup -->
                <div class="px-3 py-2 border-b border-slate-100 mb-1">
                  <p class="text-[11px] font-medium text-slate-400">Signed in as</p>
                  <p class="text-xs font-bold text-slate-800 truncate">
                    {{ authData.username ? `@${authData.username}` : authData.email }}
                  </p>
                </div>

                <MenuItem v-slot="{ active }">
                  <router-link
                    :to="{ name: 'Profile' }"
                    :class="[
                      active ? 'bg-slate-100 text-slate-900' : 'text-slate-700',
                      'flex items-center gap-2 px-3 py-2 rounded-xl text-xs font-medium transition-colors',
                    ]"
                  >
                    <svg class="h-4 w-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                    </svg>
                    <span>Your Profile</span>
                  </router-link>
                </MenuItem>

                <MenuItem v-slot="{ active }">
                  <router-link
                    :to="{ name: 'Dashboard' }"
                    :class="[
                      active ? 'bg-slate-100 text-slate-900' : 'text-slate-700',
                      'flex items-center gap-2 px-3 py-2 rounded-xl text-xs font-medium transition-colors',
                    ]"
                  >
                    <svg class="h-4 w-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
                    </svg>
                    <span>Dashboard</span>
                  </router-link>
                </MenuItem>

                <div class="h-[1px] bg-slate-100 my-1"></div>

                <MenuItem v-slot="{ active }">
                  <button
                    @click="logOutUtil"
                    :class="[
                      active ? 'bg-rose-50 text-rose-700' : 'text-rose-600',
                      'flex w-full items-center gap-2 px-3 py-2 rounded-xl text-xs font-medium transition-colors',
                    ]"
                  >
                    <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                    </svg>
                    <span>Sign out</span>
                  </button>
                </MenuItem>
              </MenuItems>
            </transition>
          </Menu>

          <!-- Guest login shortcut if not logged in -->
          <div v-else class="hidden sm:flex items-center gap-2">
            <router-link
              :to="{ name: 'Login' }"
              class="px-4 py-2 text-xs font-semibold text-neutral-300 hover:text-white transition"
            >
              Sign In
            </router-link>
            <router-link
              :to="{ name: 'Register' }"
              class="px-4 py-2 rounded-xl bg-primary text-accent text-xs font-semibold hover:bg-secondary transition shadow-sm"
            >
              Get Started
            </router-link>
          </div>
        </div>

      </div>
    </div>

    <!-- Mobile menu panel -->
    <DisclosurePanel class="sm:hidden border-t border-neutral-800 bg-neutral-950/95 backdrop-blur-md">
      <div class="px-3 pt-3 pb-4 space-y-1">
        <template v-if="authData">
          <router-link
            v-for="item in authMenu"
            :key="item.name"
            :to="{ name: item.name }"
            :class="[
              isCurrentRoute(item.name)
                ? 'bg-neutral-800 text-white font-semibold'
                : 'text-neutral-300 hover:bg-neutral-800/60 hover:text-white font-medium',
              'block px-3.5 py-2.5 rounded-xl text-sm transition-all',
            ]"
            :aria-current="isCurrentRoute(item.name) ? 'page' : undefined"
          >
            {{ item.path }}
          </router-link>
          
          <div class="pt-2 mt-2 border-t border-neutral-800/80">
            <button
              @click="logOutUtil"
              class="flex w-full items-center gap-2 px-3.5 py-2.5 rounded-xl text-sm font-medium text-rose-400 hover:bg-rose-950/30 hover:text-rose-300 transition"
            >
              <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
              <span>Log Out</span>
            </button>
          </div>
        </template>

        <template v-else>
          <router-link
            v-for="item in navigation"
            :key="item.name"
            :to="{ name: item.name }"
            :class="[
              isCurrentRoute(item.name)
                ? 'bg-neutral-800 text-white font-semibold'
                : 'text-neutral-300 hover:bg-neutral-800/60 hover:text-white font-medium',
              'block px-3.5 py-2.5 rounded-xl text-sm transition-all',
            ]"
            :aria-current="isCurrentRoute(item.name) ? 'page' : undefined"
          >
            {{ item.name }}
          </router-link>
        </template>
      </div>
    </DisclosurePanel>
  </Disclosure>
</template>

<script setup>
import { computed } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useAuth } from "../store/auth";
import logo from "../assets/1.png";
import {
  Disclosure,
  DisclosureButton,
  DisclosurePanel,
  Menu,
  MenuButton,
  MenuItem,
  MenuItems,
} from "@headlessui/vue";
import { MenuIcon, XIcon } from "@heroicons/vue/outline";

const navigation = [
  { name: "Home", path: "Home", current: false },
  { name: "Login", path: "/login", current: false },
  { name: "Register", path: "/register", current: false },
];

const authMenu = [
  { name: "Home", path: "Home", current: false },
  { name: "Dashboard", path: "Dashboard", current: false },
  { name: "Profile", path: "Profile", current: false },
  { name: "Users", path: "Users", current: false },
  { name: "MyQuestions", path: "My Questions", current: false },
  { name: "MyAnswers", path: "My Answers", current: false },
];

const auth = useAuth();
const router = useRouter();
const route = useRoute();

const authData = computed(() => {
  return auth.getAuthData;
});

const isCurrentRoute = (routeName) => {
  return route.name === routeName;
};

const logOutUtil = () => {
  auth.logout();
};
</script>