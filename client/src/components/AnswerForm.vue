<template>
    <form class="space-y-6" @submit="handleSubmit">
        <h2 class="text-lg text-center font-medium leading-6 text-white bg-primary p-4">
            Answer Form
        </h2>

        <div>
            <label for="body" class="block text-sm font-medium text-gray-700">
                Type Your Answer
            </label>
            <div class="mt-1">
                <textarea id="body" name="body" v-model="body" rows="4"
                    placeholder="Enter Question Description"
                    class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-secondary focus:border-primary text-secondary sm:text-sm">
                </textarea>
            </div>
        </div>

        <div class="text-center">
            <button type="submit"
                class="py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-secondary hover:bg-primary focus:outline-none focus:ring-2 focus:ring-offset-2">
                Add Answer
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
    },
    addAnswer: {
        type: Function,
        required: true
    }
});

const body = ref('');
const errors = ref([]);
const { closeModal, addAnswer } = props;

function handleSubmit(e) {
    e.preventDefault();
    errors.value = [];
    if (!body.value) {
        errors.value.push('Question is required');
    }
    if (errors.value.length > 0) {
        return;
    } else {
        console.log('Form submitted');
        addAnswer({
            body: body.value,
        });
        closeModal();
    }
}
</script>