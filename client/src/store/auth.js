import { defineStore } from "pinia";
import { ref } from "vue";
import router from "../routes";
import httpClient from "../plugins/interceptor";
import { useToast } from "vue-toastification";

const toast = useToast();

export const useAuth = defineStore("auth", {
  state: () => ({
    authData: JSON.parse(localStorage.getItem("user")) || null,
    profileData: null,
    loading: ref(false),
  }),

  getters: {
    getAuthData() {
      return this.authData;
    },
    getProfileData() {
      return this.profileData;
    },
    isLoading() {
      return this.loading;
    },
  },

  actions: {
    async loginAction(loginData) {
      try {
        const response = await httpClient.post("login", loginData);
        if (response.data) {
          this.authData = response.data;
          toast.success("Login successful!");
          localStorage.setItem("user", JSON.stringify(response.data));
          router.push("/dashboard");
        }
      } catch (error) {
        console.log(error);
        return error;
      }
    },

    async registerAction(registerData) {
      try {
        const response = await httpClient.post("register", registerData);
        if (response.data) {
          this.authData = response.data;
          toast.success("Registration successful!");
          localStorage.setItem("user", JSON.stringify(response.data));
          router.push("/dashboard");
        }
      } catch (error) {
        console.log(error);
        return error;
      }
    },

    async getProfileDataAction() {
      try {
        const headers = {
          Authorization: `Bearer ${this.authData.access}`,
        };
        this.loading = true;
        const response = await httpClient.get("profile", { headers });
        if (response.data) {
          this.profileData = response.data;
          this.loading = false;
        }
      } catch (error) {
        console.log(error);
        this.loading = false
        return error;
      }
    },

    async updateProfileDataAction(profileData) {
      try {
        const headers = {
          Authorization: `Bearer ${this.authData.access}`,
        };
        console.log('Update Profile Data', headers)
        this.loading = true;
        const response = await httpClient.put("profile", profileData, { headers });
        if (response.data) {
          this.profileData = response.data;
          this.loading = false;
        }
      } catch (error) {
        console.log(error);
        this.loading = false
        return error;
      }
    },

    async changePassword (passwordData) {
      try {
        const headers = {
          Authorization: `Bearer ${this.authData.access}`,
        };
        this.loading = true;
        const response = await httpClient.put("change-password", passwordData, { headers });
        if (response.status === 204) {
          this.loading = false;
          toast.success("Password changed successfully!");
        }
      } catch (error) {
        console.log(error);
        this.loading = false
        return error;
      }
    },

    logout() {
      this.authData = null;
      localStorage.removeItem("user");
      router.push("/login");
      toast.success("Logout successful!");
    },

    resetAuth() {
      this.authData = {};
    },
  },
});
