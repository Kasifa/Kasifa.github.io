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
  const title = "三维 Navier–Stokes 全局正则性问题";
  const description =
    "我记录对三维不可压缩 Navier–Stokes 全局正则性问题的梳理、计算和未解决步骤。";

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
      alternateLocale: ["en_US"],
      url: "/",
      title,
      description,
      images: [
        {
          url: "/og.png",
          width: 1536,
          height: 1024,
          alt: "三维 Navier–Stokes 全局正则性问题",
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
