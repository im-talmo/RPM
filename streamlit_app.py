import streamlit as st
import pandas as pd

# 1. 웹 페이지 기본 설정
st.set_page_config(page_title="모터 전력량 계산기", page_icon="⚙️", layout="centered")

st.title("⚙️ 멀티 RPM 모터 전력량 계산 시스템")
st.markdown("### 조건: 토크 **1 N·m** 고정 / 모터 효율 **80%** 고정")
st.write("원하는 회전수(RPM)를 3개 입력하시면 필요한 최소 전력량을 실시간으로 계산합니다.")

st.divider()

# 2. 세션 상태(Session State)를 이용해 입력 데이터 관리
if 'rpm_inputs' not in st.session_state:
    st.session_state.rpm_inputs = ["300", "500", "1200"] # 초기 기본값

# 사용자 입력창 (3회 반복 입력)
st.subheader("🔢 RPM 입력 (총 3회)")
cols = st.columns(3)
user_rpms = []

for i in range(3):
    with cols[i]:
        val = st.text_input(
            f"{i+1}번째 RPM", 
            value=st.session_state.rpm_inputs[i], 
            key=f"rpm_in_{i}"
        )
        user_rpms.append(val)

st.divider()

# 3. 데이터 처리 및 리스트, 조건문, 반복문 활용
results = []
has_error = False

# 반복문으로 3개의 입력값 처리
for idx, item in enumerate(user_rpms):
    item = item.strip()
    if not item:
        st.warning(f"⚠️ {idx+1}번째 값을 입력해 주세요.")
        has_error = True
        continue
        
    # [조건문] 예외 처리: 문자가 입력되었을 때 판단
    try:
        rpm = float(item)
        
        # [조건문] 유효성 검사: 0 이하의 숫자 판단
        if rpm > 0:
            torque = 1.0
            efficiency = 0.8
            
            # 계산 공식 적용
            mech_power = (torque * rpm) / 9.55
            elec_power = mech_power / efficiency
            
            # [리스트] 결과 데이터를 딕셔너리 형태로 추가
            results.append({
                "회차": f"{idx+1}회차",
                "회전수 (RPM)": rpm,
                "기계적 출력 (W)": round(mech_power, 2),
                "최소 필요 전기전력 (W)": round(elec_power, 2)
            })
        else:
            st.error(f"❌ {idx+1}번째 오류: RPM은 0보다 커야 합니다. (입력값: {item})")
            has_error = True
    except ValueError:
        st.error(f"❌ {idx+1}번째 오류: 숫자가 아닌 문자가 포함되어 있습니다. (입력값: {item})")
        has_error = True

# 4. 결과 출력
if not has_error and len(results) == 3:
    st.subheader("📊 계산 결과")
    
    # 데이터프레임 변환 후 표로 출력
    df = pd.DataFrame(results)
    st.dataframe(df.set_index("회차"), use_container_width=True)
    
    # 시각화 차트 추가 (RPM 대비 필요 전력량 선그래프)
    st.subheader("📈 RPM별 필요 전기전력 추이")
    chart_data = df.set_index("회전수 (RPM)")["최소 필요 전기전력 (W)"]
    st.line_chart(chart_data)