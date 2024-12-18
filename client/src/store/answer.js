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
    async addAnswer(answerData) {
      try {
        const headers = {
          Authorization: `Bearer ${auth.authData.access}`,
        };
        const response = await httpClient.post("answers", answerData, {
          headers,
        });
        toast.success("Answer added!");
      } catch (error) {
        console.log(error);
        return error;
      }
    },

    async updateAnswer(answerData) {
      try {
        const headers = {
          Authorization: `Bearer ${auth.authData.access}`,
        };
        const response = await httpClient.put(`answers${AnswerData.id}`, answerData, {
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

    async deleteAnswer(AnswerId) {
      try {
        const headers = {
          Authorization: `Bearer ${auth.authData.access}`,
        };
        const response = await httpClient.delete("answers/" + AnswerId, {
          headers,
        });
        toast.success("Answer deleted!");
      } catch (error) {
        console.log(error);
        return error;
      }
    },

    resetAnswerData() {
      this.answer = {};
      this.answers = [];
    },
  },
});