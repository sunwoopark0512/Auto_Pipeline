package main
import ("github.com/tetratelabs/wazero/api"; "encoding/json")
type FeatureReq struct {UserID string `json:"user_id"`}
type FeatureResp struct {Clicks5m int `json:"clicks_5m"`}

func getFeatures(user string) FeatureResp {
  // call DAX via Lambda URL (simplified)
  return FeatureResp{Clicks5m: 3}
}
func main() {
  api.RegisterFunction("handle", func(ctx api.Context, m api.Module, p, s uint32) {
     data, _ := m.Memory().Read(p, s)
     var req FeatureReq; json.Unmarshal(data, &req)
     resp := getFeatures(req.UserID)
     out, _ := json.Marshal(resp)
     p2, _ := m.Memory().Allocate(uint32(len(out)))
     m.Memory().Write(p2, out)
     ctx.SetReturnValues(p2, uint32(len(out)))
  })
}

