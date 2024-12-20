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
    questionData: ref({}),
    loading: ref(false),
  }),

  getters: {
    getQuestion() {
      return this.question;
    },
    getQuestions() {
      return this.questionData;
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
        this.loading = true;
        const response = await httpClient.post("questions", QuestionData, {
          headers,
        });
        if (response.status === 201) {
          this.loading = false;
          toast.success("Question added!");
        }
      } catch (error) {
        console.log(error);
        this.loading = false;
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

    async getQuestionsAction(search = "", page = 1) {
      try {
        const headers = {
          Authorization: `Bearer ${auth.authData.access}`,
        };
        const response = await httpClient.get(`questions?page=${page}&search=${search}`, {
          headers,
        });
        console.log(response.data);
        this.questionData = response.data;
      } catch (error) {
        console.log(error);
        return error
      }
    },

    async rateQuestion(payload) {
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