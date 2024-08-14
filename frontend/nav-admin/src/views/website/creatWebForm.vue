<script setup lang="ts">
import { ref, onMounted } from "vue";
import { getCategories, CategoryResult } from "@/api/category";

// 声明 props 类型
export interface creatFormProps {
  formInline: {
    web_id: any;
    url: any;
    name: string;
    order: number;
    category_id: string;

  };
}

// 声明 props 默认值
// 推荐阅读：https://cn.vuejs.org/guide/typescript/composition-api.html#typing-component-props
const creatprops = withDefaults(defineProps<creatFormProps>(), {
  formInline: () => ({
    name: "",
    order: null,
    category_id: "",
    url: ""
  })
});

// vue 规定所有的 prop 都遵循着单向绑定原则，直接修改 prop 时，Vue 会抛出警告。此处的写法仅仅是为了消除警告。
// 因为对一个 reactive 对象执行 ref，返回 Ref 对象的 value 值仍为传入的 reactive 对象，
// 即 newFormInline === props.formInline 为 true，所以此处代码的实际效果，仍是直接修改 props.formInline。
// 但该写法仅适用于 props.formInline 是一个对象类型的情况，原始类型需抛出事件
// 推荐阅读：https://cn.vuejs.org/guide/components/props.html#one-way-data-flow
const newFormInline = ref(creatprops.formInline);

// 存储分类数据
const categories = ref<CategoryResult[]>([]);

// 获取分类数据
const fetchCategories = async () => {
  categories.value = await getCategories();
};

// 组件挂载时获取分类数据
onMounted(() => {
  fetchCategories();
});

// 更新分类ID
const handleCategoryChange = (value: string) => {
  newFormInline.value.category_id = value;
};
</script>

<template>
  <el-form :model="newFormInline">
    <el-form-item label="名称">
      <el-input
        v-model="newFormInline.name"
        class="!w-[300px]"
        placeholder="请输入网站名称"
      />
    </el-form-item>
    <el-form-item label="排序">
      <el-input
        v-model="newFormInline.order"
        type="number"
        class="!w-[300px]"
        placeholder="请输入网站排序"
      />
    </el-form-item>
    <el-form-item label="URL">
      <el-input
        v-model="newFormInline.url"
        class="!w-[300px]"
        placeholder="请输入网站url"
      />
    </el-form-item>
    <el-form-item label="分类">
      <el-select
        v-model="newFormInline.category_id"
        class="!w-[300px]"
        placeholder="请选择分类"
        @change="handleCategoryChange"
      >
        <el-option
          v-for="category in categories"
          :key="category.id"
          :label="category.name"
          :value="category.id"
        />
      </el-select>
    </el-form-item>
  </el-form>
</template>
