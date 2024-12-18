<template>
    <form class="space-y-6" @submit="handleSubmit">
        <h2 class="text-lg text-center font-medium leading-6 text-white bg-primary p-4">
            Question Form
        </h2>
        <div>
            <label for="title" class="block text-sm font-medium text-gray-700">
                Question Title
            </label>
            <div class="mt-1">
                <input id="content" name="content" v-model="content" type="text" required="" placeholder="Enter Question" autocomplete="off"
                    class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
            </div>
        </div>

        <div>
            <label for="description" class="block text-sm font-medium text-gray-700">
                Question Description
            </label>
            <div class="mt-1">
                <textarea id="description" name="description" v-model="description" rows="4"
                    placeholder="Enter Question Description"
                    class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
                </textarea>
            </div>
        </div>

        <div class="text-center">
            <button type="submit"
                class="py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-secondary hover:bg-primary focus:outline-none focus:ring-2 focus:ring-offset-2">
                Add Question
            </button>
            <button @click="closeModal"
                class="py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white mx-2 bg-accent hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2">
                Cancel
            </button>
        </div>
    </form>
</template>

<script setup>
import { ref } from 'vue';
const props = defineProps({
    closeModal: {
        type: Function,
        required: true
    }
});

const content = ref('');
const description = ref('');
const errors = ref([]);

function handleSubmit(e) {
    e.preventDefault();
    console.log(content.value, description.value);
    closeModal();
}
</script>