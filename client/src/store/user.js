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
    userData: ref({}),
    loading: ref(false),
  }),

  getters: {
    getUser() {
      return this.user;
    },
    getUsers() {
      return this.userData;
    },
    isLoading() {
      return this.loading;
    },
  },

  actions: {

    async getUserAction(username) {
      try {
        const headers = {
          Authorization: `Bearer ${auth.authData.access}`,
        };
        this.loading = true;
        const response = await httpClient.get("user/" + username, {
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

    async getUsersAction(search="", page = 1) {
      try {
        const headers = {
          Authorization: `Bearer ${auth.authData.access}`,
        };
        this.loading = true;
        const response = await httpClient.get(`users?search=${search}&page=${page}`, {
          headers,
        });
        if (response.status === 200) {
          this.userData = response.data;
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