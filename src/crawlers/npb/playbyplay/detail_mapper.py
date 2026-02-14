import re

class DetailMapper:
    @staticmethod
    def parse(detail: str) -> dict:
        result = {
            "detail": None,
            "is_hit": False,
            "rbi": 0,
            "detail_type": None,
            "hit_zone": None,
            "fielder": None,
            "fielder_sequence": None,
            "error_flag": False,
            "error_fielder": None,
        }

        if "三振" in detail:
            result["detail_type"] = "SO"
            if "空振" in detail:
                result["detail"] = "SSO"
            elif "見逃" in detail:
                result["detail"] = "LSO"

        elif "フォアボール" in detail:
            if "敬遠" in detail:
                result["detail_type"] = result["detail"] = "IB"
            else:
                result["detail_type"] = result["detail"] = "BB"
            if "打点" in detail:
                result["rbi"] = DetailMapper.get_rbi(detail)
                result["detail"] += f"_{result['rbi']}"

        elif "デッドボール" in detail:
            result["detail_type"] = result["detail"] = "HP"
            if "打点" in detail:
                result["rbi"] = DetailMapper.get_rbi(detail)
                result["detail"] += f"_{result['rbi']}"

        elif "併殺打" in detail:
            position = DetailMapper.get_position(detail)
            position_number = DetailMapper.get_position_number(detail)

            if position:
                result["detail_type"] = "DP"
                result["detail"] = f"{position}_DP"
                result["hit_zone"] = position
            
            if "打点" in detail:
                result["rbi"] = DetailMapper.get_rbi(detail)
                result["detail"] += f"_{result['rbi']}"

            if position_number:
                result["fielder"] = position_number

        elif "ゴロ" in detail:
            result["detail_type"] = "GO"
            position = DetailMapper.get_position(detail)
            position_number = DetailMapper.get_position_number(detail)

            if position:
                result["detail"] = f"{position}_GO"
                result["hit_zone"] = position
                if "打点" in detail:
                    result["rbi"] = DetailMapper.get_rbi(detail)
                    result["detail"] += f"_{result['rbi']}"

            if position_number:
                result["fielder"] = position_number

        elif "フライ" in detail:
            position = DetailMapper.get_position(detail)
            position_number = DetailMapper.get_position_number(detail)

            if position:
                if "犠牲" in detail:
                    result["rbi"] = DetailMapper.get_rbi(detail)
                    result["detail_type"] = "SF"
                    result["detail"] = f"{position}_SF_{result['rbi']}"
                elif "ファウル" in detail:
                    result["detail_type"] = "FF"
                    result["detail"] = f"{position}_FF"
                else:
                    result["detail_type"] = "FO"
                    result["detail"] = f"{position}_FO"
                result["hit_zone"] = position
                
            if position_number:
                result["fielder"] = position_number

        elif "ライナー" in detail:
            position = DetailMapper.get_position(detail)
            position_number = DetailMapper.get_position_number(detail)

            if position:
                result["detail_type"] = "LD"
                result["detail"] = f"{position}_LD"
                result["hit_zone"] = position
                
            if position_number:
                result["fielder"] = position_number

        elif "犠牲バント" in detail:
            position = DetailMapper.get_position(detail)
            position_number = DetailMapper.get_position_number(detail)

            if position:
                result["detail_type"] = "SH"
                result["detail"] = f"{position}_SH"
                result["hit_zone"] = position
            
            if "打点" in detail:
                result["rbi"] = DetailMapper.get_rbi(detail)
                result["detail"] += f"_{result['rbi']}"

            if position_number:
                result["fielder"] = position_number

        elif "ヒット" in detail or "ツーベース" in detail or "スリーベース" in detail or "ホームラン" in detail:
            result["is_hit"] = True
            position = DetailMapper.get_position(detail)
            position_number = DetailMapper.get_position_number(detail)

            if position:
                if position in ["LF", "CF", "RF"] and "ヒット" in detail:
                    result["detail_type"] = "OH"
                else:
                    result["detail_type"] = "IH"

                if "ツーベース" in detail:
                    result["detail_type"] = "2B"

                if "スリーベース" in detail:
                    result["detail_type"] = "3B"

                if "ホームラン" in detail:
                    result["detail_type"] = "HR"

                result["detail"] = f"{position}_{result['detail_type']}"
                result["hit_zone"] = position
            
            if "打点" in detail:
                result["rbi"] = DetailMapper.get_rbi(detail)
                result["detail"] += f"_{result['rbi']}"
                
            if position_number:
                result["fielder"] = position_number

        elif "盗塁" in detail:
            if "成功" in detail:
                result["detail_type"] = result["detail"] = "SB"

            elif "失敗" in detail:
                result["detail_type"] = result["detail"] = "CS"

            base = 1 if "一塁" in detail else 2 if "二塁" in detail else 3 if "三塁" in detail else 4 if "本塁" in detail else None
            if base:
                result["detail"] += f"_{base}"

        elif "ワイルドピッチ" in detail:
            result["detail_type"] = result["detail"] = "WP"

        elif "牽制アウト" in detail:
            result["detail_type"] = result["detail"] = "CO"
            base = 1 if "一塁" in detail else 2 if "二塁" in detail else 3 if "三塁" in detail else None
            if base:
                result["detail"] += f"_{base}"

        if "エラー" in detail:
            result["error_flag"] = True
            error_fielder = DetailMapper.get_error_fielder(detail)
            if error_fielder:
                result["error_fielder"] = error_fielder

        return result
    
    @staticmethod
    def get_position(text: str) -> str:
        position_map = {
            "ファースト": "1B",
            "セカンド": "2B",
            "サード": "3B",
            "ショート": "SS",
            "レフト": "LF",
            "左中間": "LC",
            "センター": "CF",
            "右中間": "RC",
            "ライト": "RF",
            "ピッチャー": "P",
            "キャッチャー": "C",
        }

        for jp, en in position_map.items():
            if jp in text:
                return en
        
        return None
    
    @staticmethod
    def get_position_number(text: str) -> str:
        position_map = {
            "ファースト": "3",
            "セカンド": "4",
            "サード": "5",
            "ショート": "6",
            "レフト": "7",
            "センター": "8",
            "ライト": "9",
            "ピッチャー": "1",
            "キャッチャー": "2",
        }

        for jp, num in position_map.items():
            if jp in text:
                return num
        
        return None
    
    @staticmethod
    def get_rbi(text: str) -> int:
        m = re.search(r"打点\s*([0-9]+)", text)
        if m:
            return int(m.group(1))
        return 0