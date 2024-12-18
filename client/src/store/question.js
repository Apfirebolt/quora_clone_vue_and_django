import { defineStore } from "pinia";
import { ref } from "vue";
import httpClient from "../plugins/interceptor";
import { useAuth } from "./auth";
import { useToast } from "vue-toastification";

const toast = useToast();
const auth = useAuth();

export const useQuestion = defineStore("question", {
  state: () => ({
    question: ref({}),
    questions: ref([]),
    loading: ref(false),
  }),

  getters: {
    getQuestion() {
      return this.question;
    },
    getQuestions() {
      return this.questions;
    },
    isLoading() {
      return this.loading;
    },
  },

  actions: {
    async addQuestion(QuestionData) {
      try {
        const headers = {
          Authorization: `Bearer ${auth.authData.access}`,
        };
        const response = await httpClient.post("questions", QuestionData, {
          headers,
        });
        toast.success("Question added!");
      } catch (error) {
        console.log(error);
        return error;
      }
    },

    async updateQuestion(questionData) {
      try {
        const headers = {
          Authorization: `Bearer ${auth.authData.access}`,
        };
        this.loading = true;
        const response = await httpClient.put(`questions/${questionData.slug}/`, questionData, {
          headers,
        });
        if (response.status === 200) {
          this.loading = false;
          toast.success("Question updated!");
        }
      } catch (error) {
        console.log(error);
        this.loading = false;
        return error;
      }
    },

    async getQuestionAction(slug) {
      try {
        const headers = {
          Authorization: `Bearer ${auth.authData.access}`,
        };
        const response = await httpClient.get("questions/" + slug, {
          headers,
        });
        if (response.status === 200) {
          this.question = response.data;
        }
      } catch (error) {
        console.log(error);
      }
    },

    async getQuestionsAction(page = 1) {
      try {
        const headers = {
          Authorization: `Bearer ${auth.authData.access}`,
        };
        const response = await httpClient.get("questions?page=" + page, {
          headers,
        });
        this.questions = response.data;
      } catch (error) {
        console.log(error);
        return error
      }
    },

    async deleteQuestion(slug) {
      try {
        const headers = {
          Authorization: `Bearer ${auth.authData.access}`,
        };
        const response = await httpClient.delete("questions/" + slug, {
          headers,
        });
        if (response.status === 204) {
          toast.success("Question deleted!");
        }
      } catch (error) {
        console.log(error);
        return error;
      }
    },

    resetQuestionData() {
      this.question = {};
      this.questions = [];
    },
  },
});