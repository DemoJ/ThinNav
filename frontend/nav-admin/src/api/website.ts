// 定义获取网址分类的函数
import { http } from "@/utils/http";
import { baseUrlApi } from "./utils";

export type webResult = {
  id: number;
  name: string;
  description: string;
  icon_url: string;
  url: string;
  category_id: number;
  category_name: string;
  order: number;
  // 其他字段根据你的实际 API 返回值
};

interface webData {
  name?: string;
  description?: string;
  icon_url?: string;
  url?: string;
  category_id?: number;
  order?: number;
  // 其他你需要更新的字段
}

export const getWebs = async ({
  page = 1,
  limit = 10,
  search = "" // 新增：搜索关键字参数
}: {
  page: number;
  limit: number;
  search?: string; // 搜索关键字为可选参数
}) => {
  try {
    const data = await http.request<{ data: webResult[]; total: number }>(
      "get",
      baseUrlApi("websites/"),
      {
        params: {
          skip: (page - 1) * limit, // 计算跳过的条数
          limit: limit,
          search: search || undefined // 如果有搜索关键字，则添加到请求参数中
        }
      }
    );
    return data;
  } catch (error) {
    console.error("Failed to fetch websites:", error);
    return { data: [], total: 0 }; // 返回空数据并确保分页控件正常工作
  }
};

export const updateWeb = async (webId: string, updateData: webData) => {
  try {
    const url = baseUrlApi(`websites/${webId}`);
    const data = await http.request<webData>(
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
    console.error(`Failed to update website ${webId}:`, error);
    return null;
  }
};

export const delWeb = async (webId: string) => {
  return http.request("delete", baseUrlApi(`websites/${webId}`));
};

export const creatWeb = async (creatData: webData) => {
  try {
    const url = baseUrlApi(`websites/`);
    const data = await http.request<webData>(
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
    console.error(`Failed to creat website:`, error);
    return null;
  }
};
