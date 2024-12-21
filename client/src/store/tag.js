import { defineStore } from "pinia";
import { ref } from "vue";
import httpClient from "../plugins/interceptor";
import { useAuth } from "./auth";
import { useToast } from "vue-toastification";

const toast = useToast();
const auth = useAuth();

export const useTag = defineStore("tag", {
  state: () => ({
    tag: ref({}),
    tagData: ref([]),
    loading: ref(false),
  }),

  getters: {
    getTag() {
      return this.tag;
    },
    getTags() {
      return this.tagData;
    },
    isLoading() {
      return this.loading;
    },
  },

  actions: {
    async addTag(questionSlug, tagData) {
      try {
        const headers = {
          Authorization: `Bearer ${auth.authData.access}`,
        };
        this.loading = true;
        const response = await httpClient.post(
          `tags/`,
          tagData,
          {
            headers,
          }
        );
        if (response.status === 201) {
          toast.success("Tag added!");
          this.loading = false;
        }
      } catch (error) {
        this.loading = false;
        console.log(error);
        return error;
      }
    },

    async updateTag(tagData) {
      try {
        const headers = {
          Authorization: `Bearer ${auth.authData.access}`,
        };
        this.loading = true;
        const response = await httpClient.put(
          `tags/${tagData.uuid}/`,
          tagData,
          {
            headers,
          }
        );
        if (response.status === 200) {
          this.loading = false;
          toast.success("Tag updated!");
        }
      } catch (error) {
        console.log(error);
        this.loading = false;
        return error;
      }
    },

    async getTagAction(tagId) {
      try {
        const response = await httpClient.get("tags/" + tagId);
        console.log(response);
      } catch (error) {
        console.log(error);
      }
    },

    async getTagsAction(page = 1) {
      try {
        const headers = {
          Authorization: `Bearer ${auth.authData.access}`,
        };
        this.loading = true;
        const response = await httpClient.get("tags?page=" + page, {
          headers,
        });
        if (response.status === 200) {
          this.loading = false;
          this.tagData = response.data;
        }
      } catch (error) {
        console.log(error);
        this.loading = false;
        return error;
      }
    },

    async deleteTag(tagId) {
      try {
        const headers = {
          Authorization: `Bearer ${auth.authData.access}`,
        };
        this.loading = true;
        const response = await httpClient.delete("tags/" + tagId, {
          headers,
        });
        if (response.status === 204) {
          toast.success("Tag deleted!");
        }
      } catch (error) {
        console.log(error);
        this.loading = false;
        return error;
      }
    },

    resetTagData() {
      this.tag = {};
      this.tagData = {};
    },
  },
});
