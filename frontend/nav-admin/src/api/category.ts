// 定义获取网址分类的函数
import { http } from "@/utils/http";
import { baseUrlApi } from "./utils";

export type CategoryResult = {
  id: number;
  name: string;
  icon_url: string;
  order: number;
  // 其他字段根据你的实际 API 返回值
};

interface CategoryData {
  name?: string;
  icon_url?: string;
  order?: number;
  // 其他你需要更新的字段
}

export const getCategories = async () => {
  try {
    const data = await http.request<CategoryResult[]>(
      "get",
      baseUrlApi("categories/")
    );
    return data;
  } catch (error) {
    console.error("Failed to fetch categories:", error);
    return [];
  }
};

export const updateCategory = async (
  categoryId: string,
  updateData: CategoryData
) => {
  try {
    const url = baseUrlApi(`categories/${categoryId}`);
    const data = await http.request<CategoryData>(
      "put",
      url,
      {
        headers: {
          "Content-Type": "application/json"
        }
      },
      {
        data: updateData
      }
    );
    return data;
  } catch (error) {
    console.error(`Failed to update category ${categoryId}:`, error);
    throw error; // 重新抛出错误
  }
};

export const delCategory = async (categoryId: string) => {
  return http.request("delete", baseUrlApi(`categories/${categoryId}`));
};

export const creatCategory = async (creatData: CategoryData) => {
  try {
    const url = baseUrlApi(`categories/`);
    const data = await http.request<CategoryData>(
      "post",
      url,
      {
        headers: {
          "Content-Type": "application/json"
        }
      },
      {
        data: creatData
      }
    );
    return data;
  } catch (error) {
    console.error(`Failed to creat category:`, error);
    throw error; // 重新抛出错误
  }
};
