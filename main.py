from api import APIClient


def main():
    client = APIClient()
    glm_4_flash_info = client.post_data('/api/paas/v4/chat/completions', data={"model": "glm-4-flash",
                                                                               "messages": [
                                                                                   { "role": "system", "content": "你是一位温柔的朋友" },
                                                                                   { "role": "user", "content": "告诉我，你有哪些能力" }
                                                                                ]
                                                                                })

    print("GLM-4-FLASH:", glm_4_flash_info['choices'][0]['message'])

if __name__ == "__main__":
    main()

