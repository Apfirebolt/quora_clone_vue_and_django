import { defineStore } from "pinia";
import httpClient from "../plugins/interceptor";
import { useAuth } from "./auth";
import { useToast } from "vue-toastification";

export const useQuestion = defineStore("question", {
  state: () => ({
    question: {},
    questionData: { results: [], count: 0 },
    loading: false,
  }),

  getters: {
    getQuestion: (state) => state.question,
    getQuestions: (state) => state.questionData,
    isLoading: (state) => state.loading,
  },

  actions: {
    /**
     * Helper to prepare FormData or JSON payload
     */
    preparePayload(payload) {
      if (payload instanceof FormData) {
        return payload;
      }

      const formData = new FormData();
      Object.keys(payload).forEach((key) => {
        const val = payload[key];
        if (val !== null && val !== undefined) {
          if (key === "image" && !(val instanceof File)) {
            // Skip non-file values for image if null/undefined
            return;
          }
          formData.append(key, val);
        }
      });
      return formData;
    },

    async addQuestion(payload) {
      const auth = useAuth();
      const toast = useToast();
      this.loading = true;

      try {
        const data = this.preparePayload(payload);
        const headers = {
          Authorization: `Bearer ${auth.authData?.access}`,
        };

        const response = await httpClient.post("questions", data, { headers });

        if (response.status === 201) {
          toast.success("Question posted successfully!");
          return response.data;
        }
      } catch (error) {
        const toast = useToast();
        const msg = error.response?.data?.detail || "Failed to publish question.";
        toast.error(msg);
        return Promise.reject(error);
      } finally {
        this.loading = false;
      }
    },

    async updateQuestion(slug, payload) {
      const auth = useAuth();
      const toast = useToast();
      this.loading = true;

      try {
        const data = this.preparePayload(payload);
        const headers = {
          Authorization: `Bearer ${auth.authData?.access}`,
        };

        const response = await httpClient.patch(`questions/${slug}/`, data, { headers });

        if (response.status === 200) {
          toast.success("Question updated!");
          this.question = response.data;
          return response.data;
        }
      } catch (error) {
        const toast = useToast();
        const msg = error.response?.data?.detail || "Failed to update question.";
        toast.error(msg);
        return Promise.reject(error);
      } finally {
        this.loading = false;
      }
    },

    async getQuestionAction(slug) {
      const auth = useAuth();
      this.loading = true;
      try {
        const headers = auth.authData?.access
          ? { Authorization: `Bearer ${auth.authData.access}` }
          : {};

        const response = await httpClient.get(`questions/${slug}/`, { headers });
        if (response.status === 200) {
          this.question = response.data;
        }
      } catch (error) {
        console.error("Error loading question:", error);
      } finally {
        this.loading = false;
      }
    },

    async getQuestionsAction(search = "", page = 1) {
      const auth = useAuth();
      this.loading = true;
      try {
        const headers = auth.authData?.access
          ? { Authorization: `Bearer ${auth.authData.access}` }
          : {};

        const response = await httpClient.get(`questions?page=${page}&search=${search}`, {
          headers,
        });
        this.questionData = response.data;
      } catch (error) {
        console.error("Error fetching question list:", error);
        return error;
      } finally {
        this.loading = false;
      }
    },

    async rateQuestion(payload) {
      const auth = useAuth();
      const toast = useToast();
      try {
        const headers = {
          Authorization: `Bearer ${auth.authData.access}`,
        };
        console.log('payload', payload);
        this.loading = true;
        const response = await httpClient.post("questions-like/" + payload.questionId + "/", {
          rating: payload.rating,
        }, {
          headers,
        });
        if (response.status === 200) {
          const toast = useToast();
          toast.success("Question rated!");
          this.loading = false;
        }
      } catch (error) {
        console.log(error);
        this.loading = false;
        return error;
      }
    },

    async getMyQuestionsAction() {
      const auth = useAuth();
      try {
        const headers = {
          Authorization: `Bearer ${auth.authData.access}`,
        };
        this.loading = true;
        const response = await httpClient.get("my-questions", {
          headers,
        });
        this.loading = false;
        this.questionData = response.data;
      } catch (error) {
        console.log(error);
        this.loading = false;
        return error;
      }
    },

    async deleteQuestion(slug) {
      const auth = useAuth();
      const toast = useToast();
      try {
        const headers = {
          Authorization: `Bearer ${auth.authData?.access}`,
        };
        const response = await httpClient.delete(`questions/${slug}`, { headers });
        if (response.status === 204) {
          toast.success("Question deleted!");
        }
      } catch (error) {
        toast.error("Failed to delete question.");
        return error;
      }
    },

    resetQuestionData() {
      this.question = {};
      this.questionData = { results: [], count: 0 };
    },
  },
});