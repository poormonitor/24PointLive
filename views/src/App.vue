<script setup lang="jsx">
import { ref, onMounted } from "vue";
import { get24Point } from "./24point";
import { generateRandomNumbers } from "./generate";
import ax from "axios";

const axios = ax.create({
    baseURL: "/api",
    timeout: 5000,
});

const numbers = ref([]);
const TIMEOUT = 120;
const time = ref(0);
const kings = ref([]);
const correctUsers = ref([]);
let answers = [];

const oneRound = () => {
    numbers.value = generateRandomNumbers();
    answers = get24Point(numbers.value);
    console.log(answers);
};

const updateDanmu = () => {
    axios.get("/danmu").then((res) => {
        res.data.forEach((val) => {
            console.log(val);
            if (
                answers.includes(formatString(val.content)) ||
                (val.content === "无解" && !answers.length)
            ) {
                correctUsers.value.push({
                    uid: val.uid,
                    user: val.user,
                    answer: val.content,
                });
            }
        });
    });
};

const formatString = (string) => {
    string = string.replace("÷", "/")
        .replace("（", "(")
        .replace("）", ")")
        .replace("×", "*")
        .replace("x", "*")
        .replace(" ", "")
    return string
}

const reduceTime = () => {
    time.value -= 1;
    updateDanmu();
    if (time.value < 0) {
        addKing();
        oneRound();
        correctUsers.value = [];
        time.value = TIMEOUT;
    }
    setTimeout(reduceTime, 1000);
};

const addKing = () => {
    if (!correctUsers.value.length) return;
    let king = correctUsers.value[0];
    let item = kings.value.find((item) => item.uid == king.uid);
    if (item) item.count += 1;
    else kings.value.push({ uid: king.uid, user: king.user, count: 1 });
    kings.value.sort((a, b) => b.count - a.count);
    sessionStorage.setItem("kings", JSON.stringify(kings.value));
};

onMounted(() => {
    kings.value = JSON.parse(sessionStorage.getItem("kings") || "[]");
    kings.value.sort((a, b) => b.count - a.count);
    reduceTime();
});
</script>

<template>
    <div class="mt-8 md:mt-10 text-center text-3xl md:text-4xl font-black">一起来玩二十四点</div>
    <div class="grid grid-cols-4 gap-4 items-center w-80 md:w-[32rem] mx-auto mt-4 md:mt-8 place-items-center">
        <div v-for="item in numbers">
            <span class="text-6xl md:text-7xl font-black">{{ item }}</span>
        </div>
    </div>
    <div class="text-center text-2xl mt-4 md:mt-8">
        <span>剩余时间: </span>
        <span>{{ time }}</span>
    </div>
    <div class="grid grid-cols-2 md:grid-cols-3 gap-y-6 md:gap-4 mx-4 md:mx-8 mt-8">
        <div class="md:p-4 col-span-2 md:col-span-1">
            <div class="text-2xl text-center font-black md:font-bold">规则解释</div>
            <ol class="mt-2 md:mt-6 flex flex-col md:gap-1 text-center md:text-start">
                <li>通过弹幕发送你的答案。</li>
                <li>
                    你的答案应该使用英文的括号，计算符号+-*/。
                </li>
                <li>答案不要包括多余的括号。</li>
                <li>若无解，发送弹幕“无解”。</li>
                <li>每次24点首个答对的用户将获得积分。</li>
                <li>根据用户累积的积分生成右方的榜单。</li>
            </ol>
        </div>
        <div class="md:p-4">
            <div class="text-2xl text-center font-black md:font-bold">率先正答</div>
            <div v-if="correctUsers.length">
                <div class="mt-4 md:mt-8">
                    <div class="text-center mt-4">
                        <div class="text-2xl font-black">
                            {{ correctUsers[0].user }}
                        </div>
                        <div class="text-xl font-black mt-1">
                            {{ correctUsers[0].answer }}
                        </div>
                    </div>
                </div>
                <div class="mt-8" v-if="correctUsers.length > 1">
                    <div>其他正答用户</div>
                    <div class="flex gap-2">
                        <span v-for="user in correctUsers.slice(1)">
                            {{ user.user }}
                        </span>
                    </div>
                </div>
            </div>
            <div class="text-center text-xl mt-10" v-else>无</div>
        </div>
        <div class="md:p-4">
            <div class="text-2xl text-center font-black md:font-bold">正答榜单</div>
            <div class="md:mt-4">
                <div class="flex gap-2 justify-center" v-for="king in kings.length">
                    <span>{{ king }}</span>
                    <span class="whitespace-nowrap font-black">
                        {{ kings[king - 1].user }}
                    </span>
                    <span>{{ kings[king - 1].count }}</span>
                </div>
            </div>
        </div>
    </div>
</template>

<style>
body {
    background: linear-gradient(-45deg, #f2fdc9, #deffc6, #caf1ff, #aaffeb);
    background-size: 400% 400%;
    animation: gradient 15s ease infinite;
    height: 100vh;
    font-weight: 700;
    overflow-y: hidden;
}

@keyframes gradient {
    0% {
        background-position: 0% 50%;
    }

    50% {
        background-position: 100% 50%;
    }

    100% {
        background-position: 0% 50%;
    }
}
</style>
