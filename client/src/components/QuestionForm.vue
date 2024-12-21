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
                {{ props.question ? 'Update' : 'Add' }} Question
            </button>
            <button @click="closeModal"
                class="py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white mx-2 bg-accent hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2">
                Cancel
            </button>
        </div>
    </form>
</template>

<script setup>
import { ref, onMounted } from 'vue';
const props = defineProps({
    closeModal: {
        type: Function,
        required: true
    },
    addQuestion: {
        type: Function,
        required: true
    },
    updateQuestion: {
        type: Function,
        required: false
    },
    question: {
        type: Object,
        default: null,
        required: false
    }
});

const content = ref('');
const description = ref('');
const errors = ref([]);
const { closeModal, addQuestion } = props;

function handleSubmit(e) {
    e.preventDefault();
    errors.value = [];
    if (!content.value) {
        errors.value.push('Question is required');
    }
    if (!description.value) {
        errors.value.push('Description is required');
    }
    if (errors.value.length > 0) {
        return;
    } else {
        console.log('Form submitted');
        if (props.question) {
            props.updateQuestion(
                content.value,
                description.value
            );
        } else {
            addQuestion({
                content: content.value,
                description: description.value
            });
        }
        closeModal();
    }
}

onMounted(() => {
    if (props.question) {
        content.value = props.question.content;
        description.value = props.question.description;
    }
    console.log('Question Form mounted');
});
</script>