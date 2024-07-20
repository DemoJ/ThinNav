<script setup lang="tsx">
import { message } from "@/utils/message";
import { useRenderIcon } from "@/components/ReIcon/src/hooks";
import AddFill from "@iconify-icons/ri/add-circle-line";
import { getCategories, updateCategory } from "@/api/category";
import { onMounted, ref } from "vue";
import forms, { type FormProps } from "./form.vue";
import {
  addDialog,
  closeDialog,
  updateDialog,
  closeAllDialog
} from "@/components/ReDialog";

defineOptions({
  // name 作为一种规范最好必须写上并且和路由的name保持一致
  name: "Category"
});

const categoryData = ref([]);

const columns: TableColumnList = [
  {
    label: "名称",
    prop: "name"
  },
  {
    label: "图标",
    prop: "icon_url"
  },
  {
    label: "排序",
    prop: "order"
  },
  {
    label: "操作",
    slot: "operation"
  }
];

function handleEdit(row) {
  addDialog({
    width: "30%",
    title: "编辑分类",

    contentRenderer: () => forms,
    props: {
      // 赋默认值
      formInline: {
        name: row.name,
        icon: row.icon_url,
        order: row.order
      }
    },
    closeCallBack: async ({ options, args }) => {
      // options.props 是响应式的
      const { formInline } = options.props as FormProps;
      const text = `名称：${formInline.name} 排序：${formInline.order}`;
      if (args?.command === "cancel") {
        // 您点击了取消按钮
        message(`您点击了取消按钮，当前表单数据为 ${text}`);
      } else if (args?.command === "sure") {
        // 假设这里得到更新后的数据
        const updatedData = {
          name: formInline.name,
          icon_url: formInline.icon,
          order: Number(formInline.order)
        };
        console.log("Updated id:", row.id);
        console.log("Updated data:", updatedData);

        const updatedCategory = await updateCategory(row.id, updatedData);

        if (updatedCategory) {
          console.log("Category updated successfully:", updatedCategory);
        } else {
          console.log("Failed to update category");
        }

        message(`您点击了确定按钮，当前表单数据为 ${text}`);
      }
    }
  });
}

const handleDelete = row => {
  message(`您删除了数据`);
};

// 页面挂载时执行操作
onMounted(async () => {
  categoryData.value = await getCategories();
  console.log(categoryData.value);
});
</script>

<template>
  <el-card shadow="never">
    <div>
      <el-button :icon="useRenderIcon(AddFill)">新建分类</el-button>
    </div>
    <pure-table :data="categoryData" :columns="columns">
      <template #operation="{ row }">
        <el-button size="small" @click="handleEdit(row)">编辑</el-button>
        <el-button size="small" type="danger" @click="handleDelete(row)">
          删除
        </el-button>
      </template>
    </pure-table>
  </el-card>
</template>
