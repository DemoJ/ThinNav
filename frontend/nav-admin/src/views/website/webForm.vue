<script setup lang="ts">
import { computed, ref, onMounted } from "vue";
import { getCategories, CategoryResult } from "@/api/category";
import { uploadIcon, getIconUrl } from "@/api/icon";

// 声明 props 类型
export interface FormProps {
  formInline: {
    web_id: any;
    url: any;
    description: any;
    name: string;
    icon: string;
    order: number;
    category_id: string;
  };
}

// 声明 props 默认值
const props = withDefaults(defineProps<FormProps>(), {
  formInline: () => ({
    name: "",
    icon: "",
    order: null,
    description: "",
    category_id: "",
    url: ""
  })
});

const newFormInline = ref(props.formInline);

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

// 获取URL地址对应的图标
const fetchIconFromUrl = async () => {
  // 假设有一个接口可以获取图标地址
  try {
    const iconUrl = await getIconUrl(newFormInline.value.url);
    newFormInline.value.icon = iconUrl.icon_url;
  } catch (error) {
    console.error("获取图标失败:", error);
  }
};

// 处理图标上传
const handleIconUpload = async (event: Event) => {
  const input = event.target as HTMLInputElement;
  const file = input.files?.[0];
  if (file) {
    try {
      const formData = new FormData();
      formData.append("file", file);

      // 调用上传图标的 API
      const response = await uploadIcon(formData);
      console.log("上传图标成功:", response.icon_url);
      newFormInline.value.icon = response.icon_url; // 仅更新本地状态中的图标 URL
    } catch (error) {
      console.error("上传图标失败:", error);
    }
  }
};

const VITE_PUBLIC_PATH = import.meta.env.VITE_PUBLIC_PATH || "/";

const processRelativePath = (path: string) => {
  if (path.startsWith("./")) {
    const basePath = import.meta.env.PROD ? "/" : VITE_PUBLIC_PATH;
    return `/api${basePath}${path.slice(2)}`;
  }
  return path;
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
    <el-form-item label="URL">
      <el-input
        v-model="newFormInline.url"
        class="!w-[300px]"
        placeholder="请输入网站url"
      />
    </el-form-item>
    <el-form-item label="图标">
      <div class="flex items-center space-x-4">
        <img
          :src="processRelativePath(newFormInline.icon)"
          alt="icon"
          class="w-12 h-12"
        />
        <el-button type="primary" size="small" @click="fetchIconFromUrl">
          获取图标
        </el-button>
        <el-button size="small" class="relative overflow-hidden">
          上传图标
          <input
            type="file"
            accept="image/*"
            class="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
            @change="handleIconUpload"
          />
        </el-button>
      </div>
    </el-form-item>
    <el-form-item label="排序">
      <el-input
        v-model="newFormInline.order"
        type="number"
        class="!w-[300px]"
        placeholder="请输入网站排序"
      />
    </el-form-item>
    <el-form-item label="描述">
      <el-input
        v-model="newFormInline.description"
        type="textarea"
        class="!w-[300px]"
        placeholder="请输入网站描述"
        rows="4"
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
