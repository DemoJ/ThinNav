<script setup lang="ts">
import { ref, onMounted, watch } from "vue";
import { debounce } from "lodash-es"; // 引入 debounce 函数
import { getWebs } from "@/api/website";
import { useRenderIcon } from "@/components/ReIcon/src/hooks";
import AddFill from "@iconify-icons/ri/add-circle-line";
import SearchIcon from "@iconify-icons/ri/search-line"; // 引入搜索图标
import {
  handleEdit,
  handleDelete,
  handleCreat,
  setFetchWebsMethod
} from "./webOperate";
import { getCategories } from "@/api/category"; // 引入获取分类的 API

const webData = ref([]);
const pagination = ref({ current: 1, pageSize: 10, total: 0 });
const searchKeyword = ref("");
const categories = ref([]); // 存储分类数据
const selectedCategory = ref(null); // 存储选中的分类

// 获取分类数据
const fetchCategories = async () => {
  try {
    // 直接将 API 返回值赋给 categories
    categories.value = await getCategories();
    console.log("分类数据获取成功：", categories.value); // 调试输出获取的数据
  } catch (error) {
    console.error("获取分类数据失败：", error);
  }
};

// 在组件挂载时获取分类
onMounted(() => {
  fetchCategories(); // 确保在挂载时调用
  fetchWebs(); // 获取网址数据
  setFetchWebsMethod(fetchWebs); // 设置获取网址的方法
});

// 监听分类变化，更新网址数据
watch(selectedCategory, newCategory => {
  fetchWebs(searchKeyword.value, newCategory);
});

// 使用 debounce 优化搜索，延迟触发 API 请求
const fetchWebs = debounce(async (keyword = "", category = "") => {
  const { data, total } = await getWebs({
    page: pagination.value.current || 1,
    limit: pagination.value.pageSize || 10,
    search: keyword,
    category: category // 添加分类参数
  });
  webData.value = data;
  pagination.value.total = total;
}, 300);

// 监听 searchKeyword 值的变化并触发 fetchWebs
watch(searchKeyword, newKeyword => {
  fetchWebs(newKeyword, selectedCategory.value);
});

const onPageSizeChange = (size: number) => {
  pagination.value.pageSize = size || 10;
  pagination.value.current = 1;
};

const onCurrentChange = (current: number) => {
  pagination.value.current = current || 1;
};

const columns: TableColumnList = [
  {
    label: "名称",
    prop: "name"
  },
  {
    label: "排序",
    prop: "order"
  },
  {
    label: "描述",
    prop: "description",
    showOverflowTooltip: true // 启用文字溢出省略号和 tooltip 显示
  },
  {
    label: "分类",
    prop: "category_name"
  },
  {
    label: "操作",
    slot: "operation"
  }
];
</script>

<template>
  <el-card shadow="never">
    <div
      style="display: flex; align-items: center; justify-content: space-between"
    >
      <el-button :icon="useRenderIcon(AddFill)" @click="handleCreat()">
        新建网址
      </el-button>
      <div style="display: flex; align-items: center; gap: 16px">
        <!-- 使用 flex 布局和 gap 调整间距 -->
        <el-select
          v-model="selectedCategory"
          placeholder="选择分类"
          style="width: 200px"
          clearable
        >
          <el-option
            v-for="category in categories"
            :key="category.id"
            :label="category.name"
            :value="category.id"
          />
        </el-select>
        <el-input
          v-model="searchKeyword"
          placeholder="输入网址名称"
          style="width: 200px"
          clearable
          :suffix-icon="useRenderIcon(SearchIcon)"
        />
      </div>
    </div>
    <pure-table :data="webData" :columns="columns" class="mt-4">
      <!-- 添加上间距 -->
      <template #operation="{ row }">
        <el-button size="small" @click="handleEdit(row)"> 编辑 </el-button>
        <el-button size="small" type="danger" @click="handleDelete(row)">
          删除
        </el-button>
      </template>
    </pure-table>
    <el-pagination
      v-model:currentPage="pagination.current"
      class="float-right mt-4 mb-4"
      :page-size="pagination.pageSize"
      :total="pagination.total"
      :page-sizes="[10, 20, 50]"
      :background="true"
      layout="total, sizes, prev, pager, next, jumper"
      @size-change="onPageSizeChange"
      @current-change="onCurrentChange"
    />
  </el-card>
</template>
