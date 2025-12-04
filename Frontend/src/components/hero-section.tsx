import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";
import { Link } from "wouter";
import { Flame } from "lucide-react";
import { Skeleton } from "@/components/ui/skeleton";
import ArticleCard from "./article-card";

export default function HeroSection() {
  const { data: featuredArticle, isLoading: featuredLoading } = useQuery({
    queryKey: ["/api/featured"],
    queryFn: api.getFeaturedArticle,
  });

  const { data: trendingArticles, isLoading: trendingLoading } = useQuery({
    queryKey: ["/api/trending"],
    queryFn: () => api.getTrendingArticles(3),
  });

  const getCategoryColor = (category: string) => {
    const colorMap: Record<string, string> = {
      Technology: "bg-tech",
      Lifestyle: "bg-lifestyle",
      Sports: "bg-sports",
      Fitness: "bg-fitness",
      Food: "bg-food",
      Travel: "bg-travel",
    };
    return colorMap[category] || "bg-gray-500";
  };

  const formatDate = (date: Date | string) => {
    return new Date(date).toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      year: "numeric",
    });
  };

  return (
    <section className="bg-white dark:bg-gray-900">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid lg:grid-cols-12 gap-8">
          {/* Featured Article */}
          <div className="lg:col-span-8">
            {featuredLoading ? (
              <div className="relative">
                <Skeleton className="w-full h-96 lg:h-[500px] rounded-xl" />
                <div className="absolute bottom-6 left-6 right-6 space-y-3">
                  <Skeleton className="w-24 h-6 rounded-full" />
                  <Skeleton className="w-3/4 h-8" />
                  <Skeleton className="w-1/2 h-6" />
                  <Skeleton className="w-1/3 h-4" />
                </div>
              </div>
            ) : featuredArticle ? (
              <Link href={`/article/${featuredArticle.id}`}>
                <article className="relative group cursor-pointer">
                  <img
                    src={featuredArticle.imageUrl}
                    alt={featuredArticle.title}
                    className="w-full h-96 lg:h-[500px] object-cover rounded-xl"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-black/20 to-transparent rounded-xl"></div>
                  <div className="absolute bottom-6 left-6 right-6 text-white">
                    <span className={`inline-block px-3 py-1 text-white text-sm font-medium rounded-full mb-3 ${getCategoryColor(featuredArticle.category)}`}>
                      {featuredArticle.category}
                    </span>
                    <h2 className="text-3xl lg:text-4xl font-bold mb-3 leading-tight group-hover:text-blue-200 transition-colors">
                      {featuredArticle.title}
                    </h2>
                    <p className="text-gray-200 text-lg mb-4 line-clamp-2">
                      {featuredArticle.excerpt}
                    </p>
                    <div className="flex items-center space-x-4 text-sm">
                      <span>{featuredArticle.author}</span>
                      <span>•</span>
                      <span>{formatDate(featuredArticle.publishDate)}</span>
                      <span>•</span>
                      <span>{featuredArticle.readTime}</span>
                    </div>
                  </div>
                </article>
              </Link>
            ) : null}
          </div>

          {/* Trending Articles Sidebar */}
          <div className="lg:col-span-4">
            <div className="bg-gray-50 dark:bg-gray-800 rounded-xl p-6 border border-transparent dark:border-gray-700">
              <h3 className="text-xl font-bold mb-6 flex items-center dark:text-white">
                <Flame className="h-5 w-5 text-orange-500 mr-2" />
                Trending Now
              </h3>
              
              {trendingLoading ? (
                <div className="space-y-6">
                  {[...Array(3)].map((_, i) => (
                    <div key={i} className="pb-6 border-b border-gray-200 last:border-b-0">
                      <div className="flex space-x-4">
                        <Skeleton className="w-20 h-16 rounded-lg flex-shrink-0" />
                        <div className="flex-1 space-y-2">
                          <Skeleton className="w-16 h-4 rounded" />
                          <Skeleton className="w-full h-4" />
                          <Skeleton className="w-1/2 h-3" />
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              ) : trendingArticles && trendingArticles.length > 0 ? (
                <div className="space-y-6">
                  {trendingArticles.map((article) => (
                    <ArticleCard key={article.id} article={article} variant="compact" />
                  ))}
                </div>
              ) : (
                <p className="text-gray-500">No trending articles found.</p>
              )}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
