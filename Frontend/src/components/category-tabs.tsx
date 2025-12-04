import { useState } from "react";
import { Link } from "wouter";
import { categories, type Category } from "@shared/schema";

interface CategoryTabsProps {
  activeCategory?: Category | "all";
  onCategoryChange?: (category: Category | "all") => void;
}

export default function CategoryTabs({ activeCategory = "all", onCategoryChange }: CategoryTabsProps) {
  const getCategoryClasses = (category: Category | "all", isActive: boolean) => {
    if (isActive) {
      if (category === "all") {
        return "bg-blue-100 text-blue-700";
      }
      const colorMap: Record<string, string> = {
        Technology: "bg-purple-100 text-purple-700",
        Business: "bg-blue-100 text-blue-700",
        Science: "bg-cyan-100 text-cyan-700",
        Health: "bg-green-100 text-green-700",
        Sports: "bg-orange-100 text-orange-700",
        Entertainment: "bg-pink-100 text-pink-700",
      };
      return colorMap[category] || "bg-gray-100 text-gray-700";
    }
    
    const hoverMap: Record<string, string> = {
      all: "bg-gray-100 text-gray-700 hover:bg-gray-200",
      Technology: "bg-purple-100 text-purple-700 hover:bg-purple-200",
      Business: "bg-blue-100 text-blue-700 hover:bg-blue-200",
      Science: "bg-cyan-100 text-cyan-700 hover:bg-cyan-200",
      Health: "bg-green-100 text-green-700 hover:bg-green-200",
      Sports: "bg-orange-100 text-orange-700 hover:bg-orange-200",
      Entertainment: "bg-pink-100 text-pink-700 hover:bg-pink-200",
    };
    return hoverMap[category] || "bg-gray-100 text-gray-700 hover:bg-gray-200";
  };

  return (
    <section className="bg-white dark:bg-gray-900 border-t dark:border-gray-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex overflow-x-auto scrollbar-hide py-4 space-x-6">
          <Link href="/">
            <button
              className={`flex-shrink-0 px-6 py-2 rounded-full font-medium text-sm whitespace-nowrap transition-colors ${getCategoryClasses("all", activeCategory === "all")}`}
              onClick={() => onCategoryChange?.("all")}
            >
              All Stories
            </button>
          </Link>
          
          {categories.map((category) => (
            <Link key={category} href={`/category/${category.toLowerCase()}`}>
              <button
                className={`flex-shrink-0 px-6 py-2 rounded-full font-medium text-sm whitespace-nowrap transition-colors ${getCategoryClasses(category, activeCategory === category)}`}
                onClick={() => onCategoryChange?.(category)}
              >
                {category}
              </button>
            </Link>
          ))}
        </div>
      </div>
    </section>
  );
}
