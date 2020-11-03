from flask_restful import Resource
class qsgw_token_api(Resource):
    def get(self):
        """
        Get Information Service VM's from the Cluster
        ---
        tags:
          - Service VM
        security:
          - token_auth: ['X-Auth-Token']
        parameters:
          - name: cluster
            in: path
            required: true
            type: string
            example: cluster01
          - name: vm
            in: path
            required: true
            type: string
            example: qsgw01

        responses:
          200:
            description: Information of the VM
            examples:
              application/json:
                {
                  "return_message": "Task Done Successfully",
                  "error_message": "",
                  "return_code": 0,
                  "json_output": [{
                    "status": "down",
                    "name": "qsgw01",
                    "ip": "",
                    "cluster": "cluster01",
                    "mac": "56:6f:e8:39:00:11",
                    "id": "ae2d175f-00fd-415f-b989-b5318d0a658e"
                  }]
                }
        """
        json_msg = {'token':123}
        return {"return_code":0, "error_message":"000000000", "return_message":"111", "json_output":json_msg}
