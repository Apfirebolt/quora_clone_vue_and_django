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
    answerData: ref([]),
    loading: ref(false),
  }),

  getters: {
    getAnswer() {
      return this.answer;
    },
    getAnswers() {
      return this.answerData;
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
        this.loading = true;
        const response = await httpClient.put(`answers/${answerData.uuid}/`, answerData, {
          headers,
        });
        if (response.status === 200) {
          this.loading = false;
          toast.success("Answer updated!");
        }
      } catch (error) {
        console.log(error);
        this.loading = false;
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
        this.loading = true;
        const response = await httpClient.get("answers?page=" + page, {
          headers,
        });
        if (response.status === 200) {
          this.loading = false;
          this.answerData = response.data;
        }
      } catch (error) {
        console.log(error);
        this.loading = false;
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
          this.answerData = response.data;
          this.loading = false;
        }
      } catch (error) {
        console.log(error);
        this.loading = false;
        return error
      }
    },

    async rateAnswer(payload) {
      try {
        const headers = {
          Authorization: `Bearer ${auth.authData.access}`,
        };
        this.loading = true;
        const response = await httpClient.post("answers-like/" + payload.answerId + "/", {
          rating: payload.rating,
        }, {
          headers,
        });
        if (response.status === 200) {
          toast.success("Answer rated!");
          this.loading = false;
        }
      } catch (error) {
        console.log(error);
        this.loading = false;
        return error;
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

    async addComment(commentData) {
      try {
        const headers = {
          Authorization: `Bearer ${auth.authData.access}`,
        };
        this.loading = true;
        const response = await httpClient.post(`comments/`, commentData, {
          headers,
        });
        if (response.status === 201) {
          toast.success("Comment added!");
          this.loading = false;
        }
      } catch (error) {
        console.log(error);
        this.loading = false;
        return error;
      }
    },

    updateComment(commentId, commentData) {
      try {
        const headers = {
          Authorization: `Bearer ${auth.authData.access}`,
        };
        this.loading = true;
        httpClient.put(`comments/${commentId}/`, commentData, {
          headers,
        });
        this.loading = false;
      } catch (error) {
        console.log(error);
        this.loading = false;
        return error;
      }
    },

    deleteComment(commentId) {
      try {
        const headers = {
          Authorization: `Bearer ${auth.authData.access}`,
        };
        this.loading = true;
        httpClient.delete(`comments/${commentId}/`, {
          headers,
        });
        this.loading = false;
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