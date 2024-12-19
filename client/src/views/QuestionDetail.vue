<template>
    <header-component />
    <section class="bg-white shadow sm:rounded-lg" id="about">
        <div class="px-4 py-5 sm:p-6">
            <h2 class="text-3xl my-5 text-center text-red-800">QUESTION DETAIL</h2>
            <div class="flex justify-between">
                <div>
                    <h3 class="text-lg leading-6 font-medium text-gray-900">
                        {{ question.content }}
                    </h3>
                    <p class="my-3">
                        Asked by: {{ question.author }}
                    </p>
                </div>
                <div class="mt-2 max-w-xl text-md text-gray-500">

                    <button @click="openModal"
                        class="mt-3 inline-flex justify-center rounded-md border border-transparent bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                        Add Answer
                    </button>
                </div>
            </div>
            <div>
            <h3 class="text-xl leading-6 font-medium text-primary my-3">
                Answers
            </h3>
            <div class="mt-2 text-md text-gray-500">
                <div v-for="answer in question.answers" :key="answer.id" class="bg-gray-100 p-4 my-2 rounded-lg">
                    <p>{{ answer.body }}</p>
                    <p>Answered by: {{ answer.author }}</p>
                </div>
            </div>
        </div>
        </div>
        
        <TransitionRoot appear :show="isOpen" as="template">
            <Dialog as="div" @close="closeModal" class="relative z-10">
                <TransitionChild as="template" enter="duration-300 ease-out" enter-from="opacity-0"
                    enter-to="opacity-100" leave="duration-200 ease-in" leave-from="opacity-100" leave-to="opacity-0">
                    <div class="fixed inset-0 bg-black/25" />
                </TransitionChild>

                <div class="fixed inset-0 overflow-y-auto">
                    <div class="flex min-h-full items-center justify-center p-4 text-center">
                        <TransitionChild as="template" enter="duration-300 ease-out" enter-from="opacity-0 scale-95"
                            enter-to="opacity-100 scale-100" leave="duration-200 ease-in"
                            leave-from="opacity-100 scale-100" leave-to="opacity-0 scale-95">
                            <DialogPanel
                                class="w-full max-w-md transform overflow-hidden rounded-2xl bg-white p-6 text-left align-middle shadow-xl transition-all">
                                <answer-form :closeModal="closeModal" :add-answer="addAnswer" />
                            </DialogPanel>
                        </TransitionChild>
                    </div>
                </div>
            </Dialog>
        </TransitionRoot>
    </section>
    <footer-component />
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';
import AnswerForm from '../components/AnswerForm.vue';
import { useQuestion } from "../store/question";
import { useAnswer } from "../store/answer";
import {
    TransitionRoot,
    TransitionChild,
    Dialog,
    DialogPanel,
} from '@headlessui/vue'

const isOpen = ref(false);
const questionStore = useQuestion();
const answerStore = useAnswer();
const route = useRoute();

const question = computed(() => questionStore.getQuestion);

function closeModal() {
    isOpen.value = false;
    console.log('Modal opened')
}

function openModal() {
    isOpen.value = true;
}

const addAnswer = async (answerBody) => {
    const questionSlug = route.params.slug;
    const payload = {
        body: answerBody
    };
    await answerStore.addAnswer(questionSlug, payload);
    await questionStore.getQuestionAction(questionSlug);
}

onMounted(async () => {
    const questionSlug = route.params.slug;
    await questionStore.getQuestionAction(questionSlug);
});
</script>