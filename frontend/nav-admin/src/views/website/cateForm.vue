<script setup lang="ts">
import { ref } from "vue";

// 声明 props 类型
export interface FormProps {
  formInline: {
    category_id: any;
    name: string;
    icon: string;
    order: number;
  };
}

// 声明 props 默认值
// 推荐阅读：https://cn.vuejs.org/guide/typescript/composition-api.html#typing-component-props
const props = withDefaults(defineProps<FormProps>(), {
  formInline: () => ({ name: "", icon: "", order: null })
});

// vue 规定所有的 prop 都遵循着单向绑定原则，直接修改 prop 时，Vue 会抛出警告。此处的写法仅仅是为了消除警告。
// 因为对一个 reactive 对象执行 ref，返回 Ref 对象的 value 值仍为传入的 reactive 对象，
// 即 newFormInline === props.formInline 为 true，所以此处代码的实际效果，仍是直接修改 props.formInline。
// 但该写法仅适用于 props.formInline 是一个对象类型的情况，原始类型需抛出事件
// 推荐阅读：https://cn.vuejs.org/guide/components/props.html#one-way-data-flow
const newFormInline = ref(props.formInline);
// 限制名称输入长度
const handleInput = (value: string) => {
  if (value.length > 6) {
    newFormInline.value.name = value.slice(0, 6);
  }
};
</script>

<template>
  <el-form :model="newFormInline">
    <el-form-item label="名称">
      <el-input
        v-model="newFormInline.name"
        class="!w-[300px]"
        placeholder="请输入分类名称"
        :maxlength="6"
        @input="handleInput"
      />
    </el-form-item>
    <el-form-item label="图标">
      <el-input
        v-model="newFormInline.icon"
        class="!w-[300px]"
        placeholder="请输入fontawesome图标名称"
      />
      <div style="margin-top: 5px; font-size: 12px; color: #888">
        仅支持免费库中 Solid 风格图标，
        <a
          href="https://fontawesome.com/search?o=r&m=free&s=solid"
          target="_blank"
          style="color: #409eff"
        >
          参考此页面
        </a>
      </div>
    </el-form-item>
    <el-form-item label="排序">
      <el-input
        v-model="newFormInline.order"
        type="number"
        class="!w-[300px]"
        placeholder="请输入分类排序"
      />
    </el-form-item>
  </el-form>
</template>
