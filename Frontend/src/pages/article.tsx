import { useQuery } from "@tanstack/react-query";
import { useRoute, Link } from "wouter";
import { api } from "@/lib/api";
import Header from "@/components/header";
import Footer from "@/components/footer";
import Newsletter from "@/components/newsletter";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { ArrowLeft, Heart, Share2, Calendar, Clock, User } from "lucide-react";
import { ReactElement, JSXElementConstructor, ReactNode, ReactPortal, Key } from "react";

export default function ArticlePage() {
  const [, params] = useRoute("/article/:id");
  const articleId = params?.id;

  const { data: article, isLoading, error } = useQuery({
    queryKey: ["/api/articles", articleId],
    queryFn: () => api.getArticle(articleId!),
    enabled: !!articleId,
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
      year: "numeric",
      month: "long",
      day: "numeric",
    });
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
        <Header />
        <main className="py-8">
          <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
            <Skeleton className="w-24 h-10 mb-6" />
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm overflow-hidden border border-transparent dark:border-gray-700">
              <Skeleton className="w-full h-64 md:h-96" />
              <div className="p-8 space-y-4">
                <Skeleton className="w-20 h-6 rounded-full" />
                <Skeleton className="w-full h-8" />
                <Skeleton className="w-3/4 h-8" />
                <div className="flex space-x-4">
                  <Skeleton className="w-24 h-4" />
                  <Skeleton className="w-24 h-4" />
                  <Skeleton className="w-24 h-4" />
                </div>
                <div className="space-y-3">
                  {[...Array(8)].map((_, i) => (
                    <Skeleton key={i} className="w-full h-4" />
                  ))}
                </div>
              </div>
            </div>
          </div>
        </main>
        <Footer />
      </div>
    );
  }

  if (error || !article) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
        <Header />
        <main className="py-12">
          <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">Article Not Found</h1>
            <p className="text-gray-600 dark:text-gray-400 mb-6">The article you're looking for doesn't exist.</p>
            <Link href="/">
              <Button>
                <ArrowLeft className="h-4 w-4 mr-2" />
                Back to Home
              </Button>
            </Link>
          </div>
        </main>
        <Footer />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <Header />
      <main className="py-8">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Back Button */}
          <Link href="/">
            <Button variant="ghost" className="mb-6">
              <ArrowLeft className="h-4 w-4 mr-2" />
              Back to Articles
            </Button>
          </Link>

          {/* Article Content */}
          <article className="bg-white dark:bg-gray-800 rounded-xl shadow-sm overflow-hidden border border-transparent dark:border-gray-700">
            {/* Hero Image */}
            <img
              src={article.imageUrl}
              alt={article.title}
              className="w-full h-64 md:h-96 object-cover"
            />

            {/* Article Header */}
            <div className="p-8">
              <div className="flex items-center justify-between mb-6">
                <span className={`inline-block px-3 py-1 text-white text-sm font-medium rounded-full ${getCategoryColor(article.category)}`}>
                  {article.category}
                </span>
                <div className="flex space-x-2">
                  <Button variant="outline" size="sm">
                    <Heart className="h-4 w-4 mr-1" />
                    {article.likes}
                  </Button>
                  <Button variant="outline" size="sm">
                    <Share2 className="h-4 w-4" />
                  </Button>
                </div>
              </div>

              <h1 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4 leading-tight">
                {article.title}
              </h1>

              <p className="text-xl text-gray-600 dark:text-gray-300 mb-6 leading-relaxed">
                {article.excerpt}
              </p>

              {/* Article Meta */}
              <div className="flex flex-wrap items-center space-x-6 text-sm text-gray-500 dark:text-gray-400 mb-8 pb-8 border-b dark:border-gray-700">
                <div className="flex items-center space-x-2">
                  <User className="h-4 w-4" />
                  <span>{article.author}</span>
                </div>
                <div className="flex items-center space-x-2">
                  <Calendar className="h-4 w-4" />
                  <span>{formatDate(article.publishDate)}</span>
                </div>
                <div className="flex items-center space-x-2">
                  <Clock className="h-4 w-4" />
                  <span>{article.readTime}</span>
                </div>
              </div>

              {/* Article Content */}
              <div className="prose prose-lg max-w-none">
                <div className="text-gray-700 leading-relaxed space-y-6">
                  {article.content.split('\n\n').map((paragraph: string | number | boolean | ReactElement<any, string | JSXElementConstructor<any>> | Iterable<ReactNode> | ReactPortal | null | undefined, index: Key | null | undefined) => (
                    <p key={index} className="text-base md:text-lg leading-relaxed">
                      {paragraph}
                    </p>
                  ))}
                </div>
              </div>
            </div>
          </article>

          {/* Related Articles Section */}
          <div className="mt-12">
            <h2 className="text-2xl font-bold mb-6">More from {article.category}</h2>
            <Link href={`/category/${article.category.toLowerCase()}`}>
              <Button variant="outline">
                View All {article.category} Articles
              </Button>
            </Link>
          </div>
        </div>
      </main>
      
      <Newsletter />
      <Footer />
    </div>
  );
}
