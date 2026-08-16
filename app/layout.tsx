import type { Metadata } from "next";
import { headers } from "next/headers";
import "./globals.css";

export async function generateMetadata(): Promise<Metadata> {
  const requestHeaders = await headers();
  const host = (
    requestHeaders.get("x-forwarded-host") ??
    requestHeaders.get("host") ??
    "navier-stokes-open-research.gwk8yzt4rp.chatgpt.site"
  )
    .split(",")[0]
    .trim();
  const protocol = (
    requestHeaders.get("x-forwarded-proto") ??
    (host.startsWith("localhost") ? "http" : "https")
  )
    .split(",")[0]
    .trim();
  const metadataBase = new URL(`${protocol}://${host}`);
  const title = "Navier–Stokes 开放研究日志";
  const description =
    "我整理的三维不可压缩 Navier–Stokes 研究综述、工作计划与计算笔记。";

  return {
    metadataBase,
    title,
    description,
    icons: {
      icon: "/favicon.svg",
      shortcut: "/favicon.svg",
    },
    openGraph: {
      type: "website",
      locale: "zh_CN",
      url: "/",
      title,
      description,
      images: [
        {
          url: "/og.png",
          width: 1536,
          height: 1024,
          alt: "Navier–Stokes 开放研究日志，R0.1 临界能量与 Fourier 三波结构",
        },
      ],
    },
    twitter: {
      card: "summary_large_image",
      title,
      description,
      images: ["/og.png"],
    },
  };
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="zh-CN">
      <body>{children}</body>
    </html>
  );
}
