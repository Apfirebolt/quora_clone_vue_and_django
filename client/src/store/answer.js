import { defineStore } from "pinia";
import { ref } from "vue";
import httpClient from "../plugins/interceptor";
import { useAuth } from "./auth";
import { useToast } from "vue-toastification";

const toast = useToast();
const auth = useAuth();

export const useAnswer = defineStore("answer", {
  state: () => ({
    answer: ref({}),
    answers: ref([]),
    loading: ref(false),
  }),

  getters: {
    getAnswer() {
      return this.answer;
    },
    getAnswers() {
      return this.answers;
    },
    isLoading() {
      return this.loading;
    },
  },

  actions: {
    async addAnswer(questionSlug, answerData) {
      try {
        const headers = {
          Authorization: `Bearer ${auth.authData.access}`,
        };
        this.loading = true;
        const response = await httpClient.post(`questions-new-answer/${questionSlug}/`, answerData, {
          headers,
        });
        if (response.status === 201) {
          toast.success("Answer added!");
          this.loading = false;
        }
      } catch (error) {
        this.loading = false;
        console.log(error);
        return error;
      }
    },

    async updateAnswer(answerData) {
      try {
        const headers = {
          Authorization: `Bearer ${auth.authData.access}`,
        };
        const response = await httpClient.put(`answers/${answerData.id}`, answerData, {
          headers,
        });
        toast.success("Answer updated!");
      } catch (error) {
        console.log(error);
        return error;
      }
    },

    async getAnswerAction(AnswerId) {
      try {
        const response = await httpClient.get("answers/" + AnswerId);
        console.log(response);
      } catch (error) {
        console.log(error);
        
      }
    },

    async getAnswersAction(page = 1) {
      try {
        const headers = {
          Authorization: `Bearer ${auth.authData.access}`,
        };
        const response = await httpClient.get("answers?page=" + page, {
          headers,
        });
        this.answers = response.data;
      } catch (error) {
        console.log(error);
        return error
      }
    },

    async getMyAnswersAction(page = 1) {
      try {
        const headers = {
          Authorization: `Bearer ${auth.authData.access}`,
        };
        this.loading = true;
        const response = await httpClient.get("my-answers?page=" + page, {
          headers,
        });
        if (response.status === 200) {
          this.answers = response.data;
          this.loading = false;
        }
      } catch (error) {
        console.log(error);
        this.loading = false;
        return error
      }
    },

    async deleteAnswer(AnswerId) {
      try {
        const headers = {
          Authorization: `Bearer ${auth.authData.access}`,
        };
        this.loading = true;
        const response = await httpClient.delete("answers/" + AnswerId, {
          headers,
        });
        if (response.status === 204) {
          toast.success("Answer deleted!");
        }
      } catch (error) {
        console.log(error);
        this.loading = false;
        return error;
      }
    },

    resetAnswerData() {
      this.answer = {};
      this.answers = [];
    },
  },
});