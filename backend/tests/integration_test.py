"""
통합 테스트 스크립트
프론트엔드와 백엔드 연동 테스트
"""
import requests
from datetime import datetime

# 테스트 설정
# 백엔드 Flask 서버 주소
BASE_URL = "http://127.0.0.1:8000"
FRONTEND_URL = "http://localhost:3000"


class Colors:
    """터미널 색상"""

    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    END = "\033[0m"


class IntegrationTest:
    def __init__(self):
        self.token = None
        self.user_id = None
        self.admin_token = None
        self.test_results = []

    def log(self, message, color=Colors.BLUE):
        """로그 출력"""
        print(f"{color}{message}{Colors.END}")

    def test_result(self, test_name, passed, details=""):
        """테스트 결과 기록"""
        status = "✓ PASS" if passed else "✗ FAIL"
        color = Colors.GREEN if passed else Colors.RED
        self.log(f"{status}: {test_name}", color)
        if details:
            self.log(f"  {details}", Colors.YELLOW)
        self.test_results.append(
            {"name": test_name, "passed": passed, "details": details}
        )

    # ------------------------------------------------------------------ #
    # 1. 서버 상태 확인
    # ------------------------------------------------------------------ #
    def test_1_health_check(self):
        """테스트 1: 서버 상태 확인 (/api/health)"""
        self.log("\n=== 테스트 1: 서버 상태 확인 ===")
        try:
            response = requests.get(f"{BASE_URL}/api/health", timeout=5)
            passed = response.status_code == 200
            self.test_result(
                "서버 상태 확인",
                passed,
                f"Status: {response.status_code}, Body: {response.text}",
            )
            return passed
        except Exception as e:
            self.test_result("서버 상태 확인", False, str(e))
            return False

    # ------------------------------------------------------------------ #
    # 2. 일반 로그인
    # ------------------------------------------------------------------ #
    def test_2_login(self):
        """테스트 2: 일반 로그인 및 JWT 토큰 획득"""
        self.log("\n=== 테스트 2: 일반 로그인 ===")
        try:
            # 먼저 create_test_data.py 실행으로 test@example.com 계정 생성 필요
            response = requests.post(
                f"{BASE_URL}/api/auth/login",
                json={"email": "test@example.com", "password": "password123"},
                timeout=5,
            )

            if response.status_code == 200:
                data = response.json()
                self.token = data.get("token")
                self.user_id = data.get("user", {}).get("id")
                self.test_result(
                    "일반 로그인",
                    True,
                    f"Token 획득 성공, User ID: {self.user_id}",
                )
                return True
            else:
                self.test_result(
                    "일반 로그인",
                    False,
                    f"Status: {response.status_code}, {response.text}",
                )
                return False
        except Exception as e:
            self.test_result("일반 로그인", False, str(e))
            return False

    # ------------------------------------------------------------------ #
    # 3. JWT 토큰 헤더 검증
    # ------------------------------------------------------------------ #
    def test_3_jwt_token_header(self):
        """테스트 3: JWT 토큰 헤더 자동 포함 확인"""
        self.log("\n=== 테스트 3: JWT 토큰 헤더 확인 ===")
        if not self.token:
            self.test_result(
                "JWT 토큰 헤더 확인",
                False,
                "토큰이 없습니다. 로그인 테스트를 먼저 실행하세요.",
            )
            return False

        try:
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
            }

            # 인증이 필요한 게시글 작성
            response = requests.post(
                f"{BASE_URL}/api/posts",
                headers=headers,
                json={
                    "title": "테스트 게시글 (JWT 토큰 확인)",
                    "content": "JWT 토큰 헤더 테스트용 게시글",
                    "status": "published",
                },
                timeout=5,
            )

            if response.status_code == 201:
                self.test_result("JWT 토큰 헤더 확인", True, "인증된 요청 성공")
                post_data = response.json()
                self.test_post_id = post_data.get("id")
                return True
            elif response.status_code == 401:
                self.test_result(
                    "JWT 토큰 헤더 확인", False, "401 Unauthorized: 토큰이 유효하지 않음"
                )
                return False
            else:
                self.test_result(
                    "JWT 토큰 헤더 확인",
                    False,
                    f"Status: {response.status_code}, {response.text}",
                )
                return False
        except Exception as e:
            self.test_result("JWT 토큰 헤더 확인", False, str(e))
            return False

    # ------------------------------------------------------------------ #
    # 4. 게시글 CRUD
    # ------------------------------------------------------------------ #
    def test_4_post_crud(self):
        """테스트 4: 게시글 CRUD 작업"""
        self.log("\n=== 테스트 4: 게시글 CRUD ===")
        if not self.token:
            self.test_result("게시글 CRUD", False, "토큰이 없습니다.")
            return False

        headers = {"Authorization": f"Bearer {self.token}"}
        post_id = None

        try:
            # CREATE
            self.log("  CREATE 테스트...")
            create_response = requests.post(
                f"{BASE_URL}/api/posts",
                headers=headers,
                json={
                    "title": f"통합 테스트 게시글 {datetime.now().strftime('%Y%m%d%H%M%S')}",
                    "content": "통합 테스트를 위한 게시글입니다.",
                    "status": "published",
                },
                timeout=5,
            )

            if create_response.status_code != 201:
                self.test_result(
                    "게시글 CREATE",
                    False,
                    f"Status: {create_response.status_code}, {create_response.text}",
                )
                return False

            post_id = create_response.json().get("id")
            self.test_result("게시글 CREATE", True, f"Post ID: {post_id}")

            # READ
            self.log("  READ 테스트...")
            read_response = requests.get(
                f"{BASE_URL}/api/posts/{post_id}", timeout=5
            )
            if read_response.status_code == 200:
                post_data = read_response.json()
                self.test_result(
                    "게시글 READ", True, f"제목: {post_data.get('title')}"
                )
            else:
                self.test_result(
                    "게시글 READ",
                    False,
                    f"Status: {read_response.status_code}, {read_response.text}",
                )
                return False

            # UPDATE
            self.log("  UPDATE 테스트...")
            update_response = requests.put(
                f"{BASE_URL}/api/posts/{post_id}",
                headers=headers,
                json={"title": "수정된 제목", "content": "수정된 내용"},
                timeout=5,
            )
            if update_response.status_code == 200:
                self.test_result("게시글 UPDATE", True, "게시글 수정 성공")
            else:
                self.test_result(
                    "게시글 UPDATE",
                    False,
                    f"Status: {update_response.status_code}, {update_response.text}",
                )
                return False

            # DELETE
            self.log("  DELETE 테스트...")
            delete_response = requests.delete(
                f"{BASE_URL}/api/posts/{post_id}",
                headers=headers,
                timeout=5,
            )
            if delete_response.status_code == 200:
                self.test_result("게시글 DELETE", True, "게시글 삭제 성공")
            else:
                self.test_result(
                    "게시글 DELETE",
                    False,
                    f"Status: {delete_response.status_code}, {delete_response.text}",
                )
                return False

            return True

        except Exception as e:
            self.test_result("게시글 CRUD", False, str(e))
            return False

    # ------------------------------------------------------------------ #
    # 5. 댓글 CRUD
    # ------------------------------------------------------------------ #
    def test_5_comment_crud(self):
        """테스트 5: 댓글 CRUD"""
        self.log("\n=== 테스트 5: 댓글 CRUD ===")
        if not self.token:
            self.test_result("댓글 CRUD", False, "토큰이 없습니다.")
            return False

        headers = {"Authorization": f"Bearer {self.token}"}

        try:
            # 테스트용 게시글 생성
            post_response = requests.post(
                f"{BASE_URL}/api/posts",
                headers=headers,
                json={
                    "title": "댓글 테스트용 게시글",
                    "content": "댓글 테스트",
                    "status": "published",
                },
                timeout=5,
            )
            if post_response.status_code != 201:
                self.test_result(
                    "댓글 CRUD",
                    False,
                    f"게시글 생성 실패: {post_response.status_code}, {post_response.text}",
                )
                return False

            post_id = post_response.json().get("id")

            # 댓글 작성
            comment_response = requests.post(
                f"{BASE_URL}/api/comments",
                headers=headers,
                json={"post_id": post_id, "content": "테스트 댓글입니다."},
                timeout=5,
            )

            if comment_response.status_code == 201:
                comment_id = comment_response.json().get("id")
                self.test_result(
                    "댓글 CREATE", True, f"Comment ID: {comment_id}"
                )

                # 댓글 목록 조회
                comments_response = requests.get(
                    f"{BASE_URL}/api/comments?post_id={post_id}", timeout=5
                )
                if comments_response.status_code == 200:
                    self.test_result(
                        "댓글 READ", True, "댓글 목록 조회 성공"
                    )
                else:
                    self.test_result(
                        "댓글 READ",
                        False,
                        f"Status: {comments_response.status_code}, {comments_response.text}",
                    )

                # 댓글 삭제
                delete_response = requests.delete(
                    f"{BASE_URL}/api/comments/{comment_id}",
                    headers=headers,
                    timeout=5,
                )
                if delete_response.status_code == 200:
                    self.test_result(
                        "댓글 DELETE", True, "댓글 삭제 성공"
                    )
                else:
                    self.test_result(
                        "댓글 DELETE",
                        False,
                        f"Status: {delete_response.status_code}, {delete_response.text}",
                    )

                # 테스트 게시글 삭제
                requests.delete(
                    f"{BASE_URL}/api/posts/{post_id}",
                    headers=headers,
                    timeout=5,
                )
                return True
            else:
                self.test_result(
                    "댓글 CREATE",
                    False,
                    f"Status: {comment_response.status_code}, {comment_response.text}",
                )
                return False

        except Exception as e:
            self.test_result("댓글 CRUD", False, str(e))
            return False

    # ------------------------------------------------------------------ #
    # 6. 신고 API
    # ------------------------------------------------------------------ #
    def test_6_report_api(self):
        """테스트 6: 신고 API"""
        self.log("\n=== 테스트 6: 신고 API ===")
        if not self.token:
            self.test_result("신고 API", False, "토큰이 없습니다.")
            return False

        headers = {"Authorization": f"Bearer {self.token}"}

        try:
            # 테스트용 게시글 생성
            post_response = requests.post(
                f"{BASE_URL}/api/posts",
                headers=headers,
                json={
                    "title": "신고 테스트용 게시글",
                    "content": "신고 테스트",
                    "status": "published",
                },
                timeout=5,
            )
            if post_response.status_code != 201:
                self.test_result(
                    "신고 API",
                    False,
                    f"게시글 생성 실패: {post_response.status_code}, {post_response.text}",
                )
                return False

            post_id = post_response.json().get("id")

            # 신고 생성
            report_response = requests.post(
                f"{BASE_URL}/api/reports",
                headers=headers,
                json={
                    "report_type": "post",
                    "post_id": post_id,
                    "reason": "테스트 신고 사유",
                },
                timeout=5,
            )

            if report_response.status_code == 201:
                report_id = report_response.json().get("id")
                self.test_result(
                    "신고 생성", True, f"Report ID: {report_id}"
                )

                # 중복 신고 방지 테스트
                duplicate_response = requests.post(
                    f"{BASE_URL}/api/reports",
                    headers=headers,
                    json={
                        "report_type": "post",
                        "post_id": post_id,
                        "reason": "중복 신고 테스트",
                    },
                    timeout=5,
                )
                if duplicate_response.status_code in (400, 409):
                    self.test_result(
                        "중복 신고 방지", True, "중복 신고가 차단되었습니다"
                    )
                else:
                    self.test_result(
                        "중복 신고 방지",
                        False,
                        f"Status: {duplicate_response.status_code}, {duplicate_response.text}",
                    )

                # 테스트 게시글 삭제
                requests.delete(
                    f"{BASE_URL}/api/posts/{post_id}",
                    headers=headers,
                    timeout=5,
                )
                return True
            else:
                self.test_result(
                    "신고 생성",
                    False,
                    f"Status: {report_response.status_code}, {report_response.text}",
                )
                return False

        except Exception as e:
            self.test_result("신고 API", False, str(e))
            return False

    # ------------------------------------------------------------------ #
    # 7. 관리자 API
    # ------------------------------------------------------------------ #
    def test_7_admin_api(self):
        """테스트 7: 관리자 API"""
        self.log("\n=== 테스트 7: 관리자 API ===")

        try:
            # 관리자 로그인 (create_test_data.py에서 admin@example.com 생성 가정)
            admin_response = requests.post(
                f"{BASE_URL}/api/auth/login",
                json={"email": "admin@example.com", "password": "admin123"},
                timeout=5,
            )

            if admin_response.status_code != 200:
                self.test_result(
                    "관리자 로그인",
                    False,
                    "관리자 계정이 없습니다. create_test_data.py를 실행하세요.",
                )
                return False

            self.admin_token = admin_response.json().get("token")
            admin_headers = {"Authorization": f"Bearer {self.admin_token}"}

            # 회원 목록 조회
            users_response = requests.get(
                f"{BASE_URL}/api/admin/users",
                headers=admin_headers,
                timeout=5,
            )
            if users_response.status_code == 200:
                self.test_result(
                    "관리자 - 회원 목록 조회", True, "회원 목록 조회 성공"
                )
            else:
                self.test_result(
                    "관리자 - 회원 목록 조회",
                    False,
                    f"Status: {users_response.status_code}, {users_response.text}",
                )

            # 신고 목록 조회
            reports_response = requests.get(
                f"{BASE_URL}/api/admin/reports",
                headers=admin_headers,
                timeout=5,
            )
            if reports_response.status_code == 200:
                self.test_result(
                    "관리자 - 신고 목록 조회", True, "신고 목록 조회 성공"
                )
            else:
                self.test_result(
                    "관리자 - 신고 목록 조회",
                    False,
                    f"Status: {reports_response.status_code}, {reports_response.text}",
                )

            return True

        except Exception as e:
            self.test_result("관리자 API", False, str(e))
            return False

    # ------------------------------------------------------------------ #
    # 8. OAuth 콜백 플로우 (URL 생성만 확인)
    # ------------------------------------------------------------------ #
    def test_8_oauth_callback_flow(self):
        """테스트 8: OAuth 콜백 플로우 시뮬레이션 (URL 생성 확인만)"""
        self.log("\n=== 테스트 8: OAuth 콜백 플로우 ===")
        self.log("  주의: 실제 OAuth 콜백은 브라우저에서 테스트해야 합니다.")
        self.log("  이 테스트는 OAuth URL 생성만 확인합니다.")

        try:
            # 카카오 OAuth URL 요청
            kakao_response = requests.get(
                f"{BASE_URL}/api/auth/oauth/kakao",
                timeout=5,
            )

            if kakao_response.status_code == 200:
                data = kakao_response.json()
                auth_url = data.get("auth_url")
                if auth_url and "kakao" in auth_url:
                    self.test_result(
                        "OAuth URL 생성 (카카오)", True, "OAuth URL 생성 성공"
                    )
                else:
                    self.test_result(
                        "OAuth URL 생성 (카카오)",
                        False,
                        f"유효하지 않은 URL: {auth_url}",
                    )
            else:
                self.test_result(
                    "OAuth URL 생성 (카카오)",
                    False,
                    f"Status: {kakao_response.status_code}, {kakao_response.text}",
                )
                self.log(
                    "  OAuth 설정이 필요할 수 있습니다. .env 파일을 확인하세요.",
                    Colors.YELLOW,
                )

            return True

        except Exception as e:
            self.test_result("OAuth 콜백 플로우", False, str(e))
            return False

    # ------------------------------------------------------------------ #
    # 전체 실행 & 요약
    # ------------------------------------------------------------------ #
    def run_all_tests(self):
        """모든 테스트 실행"""
        self.log("=" * 60)
        self.log("통합 테스트 시작", Colors.BLUE)
        self.log("=" * 60)

        tests = [
            self.test_1_health_check,
            self.test_2_login,
            self.test_3_jwt_token_header,
            self.test_4_post_crud,
            self.test_5_comment_crud,
            self.test_6_report_api,
            self.test_7_admin_api,
            self.test_8_oauth_callback_flow,
        ]

        for test in tests:
            try:
                test()
            except Exception as e:
                self.log(f"테스트 실행 중 오류: {e}", Colors.RED)

        self.print_summary()

    def print_summary(self):
        """테스트 결과 요약"""
        self.log("\n" + "=" * 60)
        self.log("테스트 결과 요약", Colors.BLUE)
        self.log("=" * 60)

        total = len(self.test_results)
        passed = sum(1 for r in self.test_results if r["passed"])
        failed = total - passed

        self.log(f"총 테스트: {total}", Colors.BLUE)
        self.log(f"성공: {passed}", Colors.GREEN)
        self.log(f"실패: {failed}", Colors.RED)

        if failed > 0:
            self.log("\n실패한 테스트:", Colors.RED)
            for result in self.test_results:
                if not result["passed"]:
                    self.log(
                        f"  - {result['name']}: {result['details']}",
                        Colors.RED,
                    )

        self.log("\n" + "=" * 60)


if __name__ == "__main__":
    print("\n통합 테스트를 시작합니다...")
    print("주의: 백엔드 서버가 실행 중이어야 합니다.")
    print("테스트 데이터가 필요합니다: python backend/create_test_data.py\n")

    input("계속하려면 Enter를 누르세요...")

    tester = IntegrationTest()
    tester.run_all_tests()
