<script setup lang="ts">
import { ref } from "vue";

import { streamAiChat } from "../api/stream_ai";

const props = defineProps<{ apiBaseUrl: string }>();

const question = ref("");
const thinking = ref("");
const answer = ref("");
const errorMessage = ref("");
const isLoading = ref(false);
let activeRequest: AbortController | null = null;

async function sendQuestion() {
  const message = question.value.trim();
  if (!message || isLoading.value) return;

  thinking.value = "";
  answer.value = "";
  errorMessage.value = "";
  isLoading.value = true;
  activeRequest = new AbortController();

  try {
    await streamAiChat({
      apiBaseUrl: props.apiBaseUrl,
      message,
      signal: activeRequest.signal,
      onEvent(event) {
        if (event.type === "thinking") thinking.value += event.content;
        if (event.type === "answer") answer.value += event.content;
      },
    });
  } catch (error) {
    if ((error as DOMException).name !== "AbortError") {
      errorMessage.value = error instanceof Error ? error.message : "请求失败";
    }
  } finally {
    isLoading.value = false;
    activeRequest = null;
  }
}

function stopGeneration() {
  activeRequest?.abort();
}
</script>

<template>
  <section>
    <textarea v-model="question" :disabled="isLoading" placeholder="输入问题" />
    <button :disabled="isLoading" @click="sendQuestion">发送</button>
    <button v-if="isLoading" @click="stopGeneration">停止</button>
    <pre v-if="thinking">{{ thinking }}</pre>
    <p v-if="answer">{{ answer }}</p>
    <p v-if="errorMessage" role="alert">{{ errorMessage }}</p>
  </section>
</template>
