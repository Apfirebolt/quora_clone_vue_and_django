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
                  item.current
                    ? 'bg-gray-900 text-white'
                    : 'text-white hover:bg-gray-700 hover:text-white',
                  'px-3 py-2 rounded-md text-sm font-medium',
                ]"
                :aria-current="item.current ? 'page' : undefined"
                >{{ item.path }}</router-link
              >
              <router-link
                v-if="!authData"
                v-for="item in navigation"
                :key="item.name"
                :to="{ name: item.name }"
                :class="[
                  item.current
                    ? 'bg-gray-900 text-white'
                    : 'text-white hover:bg-gray-700 hover:text-white',
                  'px-3 py-2 rounded-md text-sm font-medium',
                ]"
                :aria-current="item.current ? 'page' : undefined"
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
                  Hello, {{ authData.username ? authData.username : authData.email }}
                </span>
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
            item.current
              ? 'bg-gray-900 text-white'
              : 'text-white hover:bg-gray-700 hover:text-white block px-3 py-2 rounded-md text-base font-medium',
          ]"
          :aria-current="item.current ? 'page' : undefined"
          >{{ item.path }}</router-link
        >
        <router-link
          v-if="!authData"
          v-for="item in navigation"
          :key="item.name"
          :to="{ name: item.name }"
          :class="[
            item.current
              ? 'bg-gray-900 text-white'
              : 'text-white hover:bg-gray-700 hover:text-white block px-3 py-2 rounded-md text-base font-medium',
          ]"
          :aria-current="item.current ? 'page' : undefined"
          >{{ item.name }}</router-link
        >
        <button v-if="authData"
          @click="logOutUtil"
          class="text-gray-500 w-full hover:bg-gray-700 hover:text-white px-3 py-2 rounded-mdfont-medium"
        >
          Log Out
        </button>
      </div>
    </DisclosurePanel>
  </Disclosure>
</template>

<script setup>
import { computed } from "vue";
import { useRouter } from "vue-router";
import { useAuth } from "../store/auth";
import logo from '../assets/1.png';
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

const authData = computed(() => {
  return auth.getAuthData;
});

const logOutUtil = () => {
  auth.logout();
};

const navigateToRoute = (routeName) => {
  if (routeName) {
    router.push({ name: routeName });
  }
};
</script>
