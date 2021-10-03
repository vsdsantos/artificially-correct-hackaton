# %%
import re

# %%

text = "Marie and John are having a child. They are pretty happy about it. Heloise and Julia, on the other side, don't seem to like the idea very much. It is still a surprise for them. Still, Heloise and Julia bought a gift to Marie and John. They really loved the gift. For what hell they stand for"

text = re.sub(r'\.', r' .', text)

print(text)
# %%

text_vector = text.split(' ')
print(text_vector)
# %%
i = 0
idx = len(text_vector)

while i < idx:
    if ((text_vector[i] == "They") or (text_vector[i] == "they")):
      j = i - 1
      while j > 0:
          if text_vector[j] == ".":
              j -= 1
              break
            
          else:
              j -= 1
      
      while text_vector[j] != ".":
          if text_vector[j][0].isupper():
              print(text_vector[j])
              break
          else:
              j -= 1
        
    i += 1

#text_vector[i]=BANANA;

# # %%
# for(i=0; i<=fim; i++){
#     if(v[i]=='they'){
#         v[i]='BANANA';
#     }
# }
# %%
