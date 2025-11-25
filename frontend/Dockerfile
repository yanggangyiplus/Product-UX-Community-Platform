# Node.js 18 베이스 이미지
FROM node:18-alpine

# 작업 디렉토리 설정
WORKDIR /app

# package.json과 package-lock.json 복사
COPY package*.json ./

# 의존성 설치
RUN npm ci --only=production

# 애플리케이션 코드 복사
COPY . .

# 빌드
RUN npm run build

# 프로덕션 서버 (serve) 설치
RUN npm install -g serve

# 포트 노출
EXPOSE 3000

# 애플리케이션 실행
CMD ["serve", "-s", "dist", "-l", "3000"]
