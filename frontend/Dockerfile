# 개발 단계용 Dockerfile (Vite dev server + HMR)
# 이후 배포 시엔 `npm run build` 결과물을 nginx로 서빙하는 방식으로 교체할 것 (README TODO 참고)

FROM node:22-slim

WORKDIR /app

COPY package.json ./
RUN npm install

COPY . .

EXPOSE 5173
CMD ["npm", "run", "dev"]
