import { defineStore } from "pinia";
import { ref } from "vue";
import httpClient from "../plugins/interceptor";
import { useAuth } from "./auth";
import { useToast } from "vue-toastification";

const toast = useToast();
const auth = useAuth();

export const useUser = defineStore("user", {
  state: () => ({
    user: ref({}),
    users: ref([]),
    loading: ref(false),
  }),

  getters: {
    getUser() {
      return this.user;
    },
    getUsers() {
      return this.users;
    },
    isLoading() {
      return this.loading;
    },
  },

  actions: {

    async getUserAction(slug) {
      try {
        const headers = {
          Authorization: `Bearer ${auth.authData.access}`,
        };
        this.loading = true;
        const response = await httpClient.get("users/" + slug, {
          headers,
        });
        if (response.status === 200) {
          this.user = response.data;
          this.loading = false;
        }
      } catch (error) {
        this.loading = false;
        console.log(error);
      }
    },

    async getUsersAction(page = 1) {
      try {
        const headers = {
          Authorization: `Bearer ${auth.authData.access}`,
        };
        this.loading = true;
        const response = await httpClient.get("users?page=" + page, {
          headers,
        });
        if (response.status === 200) {
          this.users = response.data;
          this.loading = false;  
        }
      } catch (error) {
        console.log(error);
        this.loading = false;
        return error
      }
    },

    resetuserData() {
      this.user = {};
      this.users = [];
    },
  },
});