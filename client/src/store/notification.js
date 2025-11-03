import { defineStore } from "pinia";
import { ref } from "vue";
import httpClient from "../plugins/interceptor";
import { useAuth } from "./auth";

const auth = useAuth();

export const useNotification = defineStore("notification", {
  state: () => ({
    notifications: ref({}),
    loading: ref(false),
  }),

  getters: {
    getNotifications() {
      return this.notifications;
    },
    isLoading() {
      return this.loading;
    },
  },

  actions: {

    async getNotificationsAction(page = 1) {
      try {
        const headers = {
          Authorization: `Bearer ${auth.authData.access}`,
        };
        this.loading = true;
        const response = await httpClient.get("notifications?page=" + page, {
          headers,
        });
        if (response.status === 200) {
          this.loading = false;
          this.notifications = response.data;
        }
      } catch (error) {
        console.log(error);
        this.loading = false;
        return error;
      }
    },

    resetTagData() {
      this.notifications = {};
    },
  },
});
