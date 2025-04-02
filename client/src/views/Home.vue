<template>
    <header-component />
    <section class="bg-white shadow sm:rounded-lg" id="about">
        <div class="px-4 py-5 sm:p-6">
            <div class="hero-section bg-blue-50 py-10">
                <div class="text-center">
                    <h1 class="text-5xl font-bold text-blue-800">Welcome to Quora Clone</h1>
                    <p class="mt-4 text-lg text-gray-700">
                        A place to share knowledge and better understand the world.
                    </p>
                    <div class="mt-6">
                        <button class="px-6 py-3 bg-primary text-accent rounded-lg shadow hover:bg-secondary">
                            Get Started
                        </button>
                        <button class="ml-4 px-6 py-3 bg-accent text-primary rounded-lg shadow hover:bg-neutral hover:text-accent">
                            Learn More
                        </button>
                    </div>
                </div>
            </div>

            <ul class="mt-5 space-y-2 text-gray-700">
                <li class="flex items-center">
                    <span class="inline-block w-2 h-2 bg-secondary rounded-full mr-2"></span>
                    Add questions
                </li>
                <li class="flex items-center">
                    <span class="inline-block w-2 h-2 bg-secondary rounded-full mr-2"></span>
                    Answer questions
                </li>
                <li class="flex items-center">
                    <span class="inline-block w-2 h-2 bg-secondary rounded-full mr-2"></span>
                    Add comments
                </li>
                <li class="flex items-center">
                    <span class="inline-block w-2 h-2 bg-secondary rounded-full mr-2"></span>
                    Upvote and downvote questions and answers
                </li>
                <li class="flex items-center">
                    <span class="inline-block w-2 h-2 bg-secondary rounded-full mr-2"></span>
                    Authentication
                </li>
                <li class="flex items-center">
                    <span class="inline-block w-2 h-2 bg-secondary rounded-full mr-2"></span>
                    Authorization
                </li>
                <li class="flex items-center">
                    <span class="inline-block w-2 h-2 bg-secondary rounded-full mr-2"></span>
                    Profile
                </li>
                <li class="flex items-center">
                    <span class="inline-block w-2 h-2 bg-secondary rounded-full mr-2"></span>
                    Search questions and answers
                </li>
                <li class="flex items-center">
                    <span class="inline-block w-2 h-2 bg-secondary rounded-full mr-2"></span>
                    Follow Users
                </li>
                <li class="flex items-center">
                    <span class="inline-block w-2 h-2 bg-secondary rounded-full mr-2"></span>
                    Change Password
                </li>
            </ul>
        </div>
    </section>
    <footer-component />
</template>

<script setup>
</script>