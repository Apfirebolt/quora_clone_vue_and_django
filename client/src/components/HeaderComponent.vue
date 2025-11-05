<template>
  <Disclosure as="nav" class="bg-neutral" v-slot="{ open }">
    <div class="max-w-7xl mx-auto px-2 sm:px-6 lg:px-8 font-roboto">
      <div class="relative flex items-center justify-between h-16">
        <div class="absolute inset-y-0 left-0 flex items-center sm:hidden">
          <!-- Mobile menu button-->
          <DisclosureButton
            class="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-white hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white"
          >
            <span class="sr-only">Open main menu</span>
            <MenuIcon v-if="!open" class="block h-6 w-6" aria-hidden="true" />
            <XIcon v-else class="block h-6 w-6" aria-hidden="true" />
          </DisclosureButton>
        </div>
        <div
          class="flex-1 flex items-center justify-center sm:items-stretch sm:justify-start"
        >
          <div class="flex-shrink-0 flex items-center">
            <img :src="logo" alt="Logo" class="block w-8 h-8 rounded-full" />
          </div>
          <div class="hidden sm:block sm:ml-6">
            <div class="flex space-x-4">
              <router-link
                v-if="authData"
                v-for="item in authMenu"
                :key="item.name"
                :to="{ name: item.name }"
                :class="[
                  isCurrentRoute(item.name)
                    ? 'bg-gray-900 text-white border-b-2 border-blue-500'
                    : 'text-white hover:bg-gray-700 hover:text-white',
                  'px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200',
                ]"
                :aria-current="isCurrentRoute(item.name) ? 'page' : undefined"
                >{{ item.path }}</router-link
              >
              <router-link
                v-if="!authData"
                v-for="item in navigation"
                :key="item.name"
                :to="{ name: item.name }"
                :class="[
                  isCurrentRoute(item.name)
                    ? 'bg-gray-900 text-white border-b-2 border-blue-500'
                    : 'text-white hover:bg-gray-700 hover:text-white',
                  'px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200',
                ]"
                :aria-current="isCurrentRoute(item.name) ? 'page' : undefined"
                >{{ item.name }}</router-link
              >
              <button
                v-if="authData"
                @click="logOutUtil"
                class="text-gray-500 hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium"
              >
                Log Out
              </button>
            </div>
          </div>
        </div>
        <div
          class="absolute inset-y-0 right-0 flex items-center pr-2 sm:static sm:inset-auto sm:ml-6 sm:pr-0"
        >
          <!-- Profile dropdown -->
          <Menu as="div" class="ml-3 relative">
            <div>
              <MenuButton
                class="bg-gray-800 flex text-sm rounded-full focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-800 focus:ring-white"
              >
                <span class="sr-only">Open user menu</span>
                <span v-if="authData" class="text-white px-2 py-1 m-1">
                  Hello,
                  {{ authData.username ? authData.username : authData.email }}
                </span>
                <transition
                  enter-active-class="transition ease-out duration-100"
                  enter-from-class="transform opacity-0 scale-95"
                  enter-to-class="transform opacity-100 scale-100"
                  leave-active-class="transition ease-in duration-75"
                  leave-from-class="transform opacity-100 scale-100"
                  leave-to-class="transform opacity-0 scale-95"
                >
                  <MenuItems
                    class="origin-top-right absolute right-0 mt-10 w-64 rounded-md shadow-lg py-1 bg-white ring-1 ring-black ring-opacity-5 focus:outline-none"
                  >
                    <MenuItem v-slot="{ active }">
                      <router-link
                        :to="{ name: 'Profile' }"
                        :class="[
                          active ? 'bg-gray-100' : '',
                          'block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100',
                        ]"
                      >
                        Your Profile
                      </router-link>
                    </MenuItem>
                    <MenuItem v-slot="{ active }">
                      <router-link
                        :to="{ name: 'Dashboard' }"
                        :class="[
                          active ? 'bg-gray-100' : '',
                          'block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100',
                        ]"
                      >
                        Dashboard
                      </router-link>
                    </MenuItem>
                    <MenuItem v-slot="{ active }">
                      <button
                        @click="logOutUtil"
                        :class="[
                          active ? 'bg-gray-100' : '',
                          'block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100',
                        ]"
                      >
                        Sign out
                      </button>
                    </MenuItem>
                  </MenuItems>
                </transition>
              </MenuButton>
            </div>
          </Menu>
        </div>
      </div>
    </div>

    <DisclosurePanel class="sm:hidden">
      <div class="px-2 pt-2 pb-3 space-y-1">
        <router-link
          v-if="authData"
          v-for="item in authMenu"
          :key="item.name"
          :to="{ name: item.name }"
          :class="[
            isCurrentRoute(item.name)
              ? 'bg-gray-900 text-white border-l-4 border-blue-500'
              : 'text-white hover:bg-gray-700 hover:text-white',
            'block px-3 py-2 rounded-md text-base font-medium transition-colors duration-200',
          ]"
          :aria-current="isCurrentRoute(item.name) ? 'page' : undefined"
          >{{ item.path }}</router-link
        >
        <router-link
          v-if="!authData"
          v-for="item in navigation"
          :key="item.name"
          :to="{ name: item.name }"
          :class="[
            isCurrentRoute(item.name)
              ? 'bg-gray-900 text-white border-l-4 border-blue-500'
              : 'text-white hover:bg-gray-700 hover:text-white',
            'block px-3 py-2 rounded-md text-base font-medium transition-colors duration-200',
          ]"
          :aria-current="isCurrentRoute(item.name) ? 'page' : undefined"
          >{{ item.name }}</router-link
        >
        <button
          v-if="authData"
          @click="logOutUtil"
          class="text-gray-500 w-full hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md font-medium"
        >
          Log Out
        </button>
      </div>
    </DisclosurePanel>
  </Disclosure>
</template>

<script setup>
import { computed, ref } from "vue";
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
import { BellIcon, MenuIcon, XIcon } from "@heroicons/vue/outline";

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

const navigateToRoute = (routeName) => {
  if (routeName) {
    router.push({ name: routeName });
  }
};
</script>
